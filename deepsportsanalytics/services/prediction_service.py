from db.models import StatModel

class PredictionService(object):

    def __init__(self, model_storage):
        self.__model_storage = model_storage

    def predict(self, data, model_name):
        return self.__model_storage.get(model_name).predict(data)

    def update(self, data, model_name):
        # model = self.__model_storage.get(model_name)
        # model.update(data)

        model_type = StatModel.query.filter(StatModel.name == model_name=).first().type

        model_storage.set(model_name)
