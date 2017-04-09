import logging

logger = logging.getLogger(__name__)


class PredictionService(object):

    def __init__(self, model_storage):
        self.__model_storage = model_storage

    def predict(self, X, model_name):
        logger.info('predict: model_name = %s' % model_name)
        return self.__model_storage.get(model_name).predict(X)
