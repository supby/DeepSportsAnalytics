import os
import sys
import logging
import logging.config
import argparse
import ConfigParser
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from data.source.nhlreference_source import NHLRefDataSource
from utils import date_utils
from data.storage.data_repository import DataRepository

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(process)d:%(thread)d] \
                                [%(levelname)s] [%(module)s] [%(funcName)s] \
                                %(message)s')
ch.setFormatter(formatter)
root_logger.addHandler(ch)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--df')
    parser.add_argument('--dt')
    parser.add_argument('--mn')
    parser.add_argument('--dst')
    args = parser.parse_args()

    date_from = date_utils.try_parse(args.df)
    date_to = date_utils.try_parse(args.dt)
    model_name = args.mn
    data_source_type = args.dst

    config = ConfigParser.ConfigParser()
    config.read('scripts.cfg')

    ds = NHLRefDataSource(team_stat_season=2015,
                        games_season=2016,
                        cache_team_stats=True)
    X, Y, metadata = ds.load(dict(date_from=date_from, date_to=date_to))

    data_rep = DataRepository(uri=config.get('defaults', 'MONGO_URI'))
    data = []
    keys = metadata[0].keys()+['x{0}'.format(i) for i in range(len(X[0]))]+['y']
    for i in range(len(Y)):
        data_row = [metadata[i][k] for k in metadata[i].keys()]+X[i]+[Y[i]]
        doc = { keys[j]:str(data_row[j]) for j in range(len(X[i])) }
        data.append(doc)

    data_rep.add(model_name, data)
