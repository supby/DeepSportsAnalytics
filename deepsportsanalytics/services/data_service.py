import logging

logger = logging.getLogger(__name__)

class DataService(object):

    def __init__(self, data_source_factory):
        self.__data_source_factory = data_source_factory

    def get_data(self, data_source_type, filter):
        logger.info('get_data, data_source_type = %s' % data_source_type)

        data_source = self.__data_source_factory.create(data_source_type)
        X = []
        Y = []
        meta = []        
        for row in data_source.load(filter=filter):
            X.append(row['X'])
            Y.append(row['Y'])
            meta.append(row['meta'])

        return X, Y, meta
