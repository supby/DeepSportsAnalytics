import os
import sys
import logging
import logging.config
import argparse
import csv
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from data.source.nhlreference_source import NHLRefDataSource
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

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--df')
    parser.add_argument('--dt')
    parser.add_argument('--mn')
    parser.add_argument('--dst')
    parser.add_argument('--f')
    args = parser.parse_args()

    date_from = date_utils.try_parse(args.df)
    date_to = date_utils.try_parse(args.dt)
    model_name = args.mn
    data_source_type = args.dst
    csv_filename = args.f

    ds = NHLRefDataSource(team_stat_season=2015,
                        games_season=2016,
                        cache_team_stats=True)
    X, Y, metadata = ds.load(dict(date_from=date_from, date_to=date_to))

    with open(csv_filename, 'wb') as csvfile:
        datawriter = csv.writer(csvfile)
        datawriter.writerow(metadata[0].keys()+['x{0}'.format(i) for i in range(len(X[0]))]+['y'])
        for i in range(len(Y)):
            datawriter.writerow([metadata[i][k] for k in metadata[i].keys()]+X[i]+[Y[i]])
