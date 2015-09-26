''' Main model which is serialized/desirialized from DB/file '''

import logging

from statmodel.model_base import ModelBase

logger = logging.getLogger(__name__)

class ScikitModel(ModelBase):

    def __init__(self, X, Y, model, scaler=None):
        self.X = X
        self.Y = Y
        self.model = model
        self.scaler = scaler

    def __scale_data(self, X):
        X_new = X
        if self.scaler:
            logger.info('scale data.')
            X_new = self.scaler.fit_transform(X)
        return X_new

    def train(self):
        logger.info('[train]: start')

        self.model = self.model.fit(self.__scale_data(self.X), self.Y)

        logger.info('[train]: end')

    def predict(self, X):
        logger.info('predict_proba.')

        return self.model.predict_proba(self.__scale_data(X))
