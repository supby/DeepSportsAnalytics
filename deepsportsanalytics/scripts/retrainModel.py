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
from statmodel.model_factory import StatModelFactory
from data.storage.azure_storage import AzureBlobStorage

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
    parser.add_argument('--sn')
    parser.add_argument('--mn')
    parser.add_argument('--mt')
    args = parser.parse_args()
    source_name = args.sn
    model_name = args.mn
    model_type = args.mt

    config = ConfigParser.ConfigParser()
    config.read('scripts.cfg')

    root_logger.info('Get train data.')

    data_rep = DataRepository(uri=config.get('defaults', 'MONGO_URI'))
    X = []
    Y = []
    for row in data_rep.get(source_name, { '$or': [{'Y': [1]}, {'Y': [0]}]}):
        root_logger.info(row['meta'])

        X.append(row['X'])
        Y.append(row['Y'])

    root_logger.info('We have {0} rows to train'.format(len(Y)))
    root_logger.info('Train model.')

    model = StatModelFactory.create(model_type)
    model.train(X, Y)

    model_storage = AzureBlobStorage(
                    config.get('defaults', 'AZURE_STORAGE_NAME'),
                    config.get('defaults', 'AZURE_STORAGE_KEY'),
                    'deepsportmodels')
    model_storage.set(model_name, model)

    root_logger.info('Done.')
