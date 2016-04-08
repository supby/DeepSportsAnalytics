import os
import sys
import logging
import logging.config
import argparse
import ConfigParser
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from data.source.sport_reference_source import SportReferenceDataSource
from utils import date_utils
from data.storage.data_repository import DataRepository
from data.source.sport_reference_source import NBAReferenceRowParseStrategy
from data.source.sport_reference_source import NHLReferenceRowParseStrategy

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(process)d:%(thread)d] [%(levelname)s] [%(module)s] [%(funcName)s] %(message)s')
ch.setFormatter(formatter)
root_logger.addHandler(ch)

__source_type_map = {
    'NHL': NHLReferenceRowParseStrategy(),
    'NBA': NBAReferenceRowParseStrategy()
}

__source_type_base_url_map = {
    'NHL': 'http://www.hockey-reference.com',
    'NBA': 'http://www.basketball-reference.com'
}

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--df')
    parser.add_argument('--dt')
    parser.add_argument('--sn')
    parser.add_argument('--st')
    args = parser.parse_args()

    date_from = date_utils.try_parse(args.df)
    date_to = date_utils.try_parse(args.dt)
    source_name = args.sn
    source_type = args.st

    config = ConfigParser.ConfigParser()
    config.read('scripts.cfg')

    ds = SportReferenceDataSource(
                        base_url=__source_type_base_url_map[source_type],
                        team_stat_season=2015,
                        games_season=2016,
                        game_type=source_type,
                        row_parse_strategy=__source_type_map[source_type],
                        cache_team_stats=True)
    X, Y, metadata = ds.load(dict(date_from=date_from, date_to=date_to))

    data_rep = DataRepository(uri=config.get('defaults', 'MONGO_URI'))

    meta_keys = metadata[0].keys()
    for i in range(len(Y)):
        if not Y[i]:
            continue
        meta_data_row = [metadata[i][k] for k in metadata[i].keys()]
        res = data_rep.update(
            source_name,
            { 'meta.{0}'.format(meta_keys[j]):meta_data_row[j] for j in range(len(meta_keys)) },
            { 'Y': [Y[i]] }
        )
	root_logger.info(res)
