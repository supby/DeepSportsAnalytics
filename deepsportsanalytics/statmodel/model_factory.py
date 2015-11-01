import logging

from sklearn.linear_model import LogisticRegression

from statmodel.scikit_model import ScikitModel
# from statmodel.dnn_model import DNNModel

logger = logging.getLogger(__name__)

class StatModelFactory(object):
    __models_map = {
        'scikitmodel': lambda: ScikitModel(model=LogisticRegression(penalty='l2', C=0.7)),
        # 'dnn': lambda: DNNModel()
    }

    @staticmethod
    def create(model_type):
        logger.info('create: model_type = %s' % model_type)
        return StatModelFactory.__models_map.get(model_type, lambda: None)()
