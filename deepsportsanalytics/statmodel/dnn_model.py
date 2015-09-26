''' Main model which is serialized/desirialized from DB/file '''

import logging

from statmodel.model_base import ModelBase

logger = logging.getLogger(__name__)

class DNNModel(ModelBase):

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def train(self):
        pass

    def predict(self, X):
        pass
