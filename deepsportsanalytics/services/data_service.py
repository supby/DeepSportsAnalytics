import logging

logger = logging.getLogger(__name__)

class DataService(object):

    def __init__(self, data_source_factory):
        self.__data_source_factory = data_source_factory

    def get_data(self, data_source_type, filter):
        logger.info('get_data, data_source_type = %s' % data_source_type)

        data_source = self.__data_source_factory.create(data_source_type)
        return data_source.load(filter=filter)
