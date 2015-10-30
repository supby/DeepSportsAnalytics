class DataService(object):

    def __init__(self, data_storage, data_source_factory):
        self.__data_storage = data_storage
        self.__data_source_factory = data_source_factory

    def get_data(self, data_source_type, filter):
        data_source = self.__data_source_factory.create(data_source_type)
        return data_source.load(filter=filter, skip_no_score=False)
