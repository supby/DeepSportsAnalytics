
import datetime
from dateutil import parser
import csv

import global_config
from data.source.nhlreference_source import NHLRefDataSource
from data.source.source_base import DataSourceFilter
from shared.cache import DefaultCache


if __name__ == '__main__':
    date_from = datetime.datetime.date(parser.parse('2014-10-08'))
    
    data_source = NHLRefDataSource(dict(sub_data_url=global_config.MINER['sub_data_url'],
                                       base_url=global_config.MINER['base_url']),
                                       cache=DefaultCache.get_instance(),
                                       cache_team_stats=True)
        
    new_data_set, new_data_set_m = \
            data_source.load(filter=DataSourceFilter(
                                    date_from=date_from, 
                                    date_to=None,
                                    limit=-1),
                             skip_no_score=True)
    
    with open('../data/nhl_2014-2015.csv', 'w') as outcsv:
        writer = csv.writer(outcsv)
        
        X = new_data_set[0]
        Y = new_data_set[1]
        
        header = ['x%s' % i for i in range(len(X[0]))]
        header.append('y')
        writer.writerow(header)
        
        for i in range(len(X)):
            row = X[i]
            row.append(Y[i])
            writer.writerow(row)
                             
    