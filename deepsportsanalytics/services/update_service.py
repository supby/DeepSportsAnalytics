import logging

logger = logging.getLogger(__name__)

class UpdateService(object):

    def __init__(self, data_service, prediction_service, data_storage):
        self.__data_service = data_service
        self.__prediction_service = prediction_service
        self.__data_storage = data_storage

    def update(self, filter, model_name, data_source_type, reset_data):
        logger.info('update')

        new_data_set, new_data_set_m = \
            self.__data_service.get_data(
                        data_source_type=data_source_type,
                        filter=filter)

        current_dataset = ([], [])
        if not reset_data:
            current_dataset = self.__data_storage.get('traindata', ([], []))
        else:
            logger.info('reset current train data.')

        updated_dataset = (current_dataset[0] + new_data_set[0],
                           current_dataset[1] + new_data_set[1])
        self.__data_storage.set('traindata', updated_dataset)


        self.__prediction_service.update(updated_dataset[0],
                                        updated_dataset[1], model_name);
