import logging

logger = logging.getLogger(__name__)

class PredictionService(object):

    def __init__(self, model_storage, stat_model_factory, stat_model_repo):
        self.__model_storage = model_storage
        self.__stat_model_factory = stat_model_factory
        self.__stat_model_repo = stat_model_repo

    def predict(self, data, model_name):
        logger.info('predict: model_name = %s' % model_name)
        return self.__model_storage.get(model_name).predict(data)

    def update(self, data, model_name):
        logger.info('update started.')

        model_type = stat_model_repo.get_type_by_name(model_name=model_name)
        model = self.__stat_model_factory.create(model_type)
        model.train(data)

        model_storage.set(model_name, model)

        logger.info('update finished.')
