import os
import sys
import logging
import logging.config
import argparse
import csv
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from data.source.sport_reference_source import SportReferenceDataSource
from data.source.sport_reference_source import NBAReferenceRowParseStrategy
from data.source.sport_reference_source import NHLReferenceRowParseStrategy
from utils import date_utils

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(process)d:%(thread)d] \
                                [%(levelname)s] [%(module)s] [%(funcName)s] \
                                %(message)s')
ch.setFormatter(formatter)
root_logger.addHandler(ch)

__source_type_map = {
    'NHL': NHLReferenceRowParseStrategy(),
    'NBA': NBAReferenceRowParseStrategy()
}


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--df')
    parser.add_argument('--dt')
    parser.add_argument('--st')
    parser.add_argument('--bu')
    parser.add_argument('--tss')
    parser.add_argument('--gs')
    parser.add_argument('--f')
    args = parser.parse_args()

    date_from = date_utils.try_parse(args.df)
    date_to = date_utils.try_parse(args.dt)
    source_type = args.st
    team_stat_season = args.tss
    games_season = args.gs
    csv_filename = args.f
    base_url = args.bu

    ds = SportReferenceDataSource(
                        base_url=base_url,
                        team_stat_season=team_stat_season,
                        games_season=games_season,
                        game_type=source_type,
                        row_parse_strategy=__source_type_map[source_type],
                        cache_team_stats=True)
    X, Y, metadata = ds.load(dict(date_from=date_from, date_to=date_to))

    with open(csv_filename, 'wb') as csvfile:
        datawriter = csv.writer(csvfile)
        datawriter.writerow(metadata[0].keys()+['x{0}'.format(i) for i in range(len(X[0]))]+['y'])
        for i in range(len(Y)):
            datawriter.writerow([metadata[i][k] for k in metadata[i].keys()]+X[i]+[Y[i]])
