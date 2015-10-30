from statmodel.scikit_model import ScikitModel
from statmodel.dnn_model import DNNModel

class StatModelFactory(object):
    __models_map = {
        'scikitmodel': ScikitModel(model=LogisticRegression(penalty='l2', C=0.7)),
        'dnn': DNNModel()
    }

    @staticmethod
    def create(model_type):
        __models_map.get('model_type', None)
