import sys
import datetime
import logging
import datetime

from sklearn.linear_model import LogisticRegression

import global_config
from data.storage.azure_storage import AzureBlobStorage
from data.storage.storage_base import StorageBase
from data.source.nhlreference_source import NHLRefDataSource
from data.source.source_base import DataSourceFilter
from data.source.source_base import DataSourceBase
from shared.cache import DefaultCache
from statmodel.scikit_model import ScikitModel
from services.model_service_base import ModelServiceBase

logger = logging.getLogger(__name__)

class AzureModelService(ModelServiceBase):

    def __init__(self, model_storage, data_storage, data_source):

        assert isinstance(model_storage, StorageBase), \
            "model_storage have to be inherited from StorageBase"

        assert isinstance(data_storage, StorageBase), \
            "data_storage have to be inherited from StorageBase"

        assert isinstance(data_source, DataSourceBase), \
            "data_source have to be inherited from DataSourceBase"

        self.__model_storage = model_storage
        self.__data_storage = data_storage
        self.__data_source = data_source

    def update(self, date_from, date_to, reset_data=False):
        logger.info('[update]: date_from=%s, date_to=%s' % (date_from, date_to))

        updated_dataset = self.__get_new_data(date_from, date_to, reset_data)
        model = ScikitModel(updated_dataset[0],
                                 updated_dataset[1],
                                 LogisticRegression(penalty='l2', C=0.7))
        model.train()
        self.__model_storage.set('model', model)

    def predict(self, date_predict_from, date_predict_to):

        logger.info('[predict]: date_predict_from=%s, date_predict_to=%s'
                                        % (date_predict_from, date_predict_to))

        data_to_predict, data_to_predict_m = \
            self.__data_source.load(filter=DataSourceFilter(
                                date_from=date_predict_from,
                                date_to=date_predict_to,
                                limit=-1),
                             skip_no_score=False)

        if len(data_to_predict[0]) == 0:
            return None, None, None

        predictions = self.__model_storage.get('model')\
                                          .predict(data_to_predict[0])

        return data_to_predict, data_to_predict_m, predictions

    def status(self):
        pass

    def __get_new_data(self, date_from, date_to, reset_data):

        new_data_set, new_data_set_m = self.__data_source.load(
                            filter=DataSourceFilter(
                                            date_from=date_from,
                                            date_to=date_to,
                                            limit=-1),
                            skip_no_score=True)

        current_dataset = ([], [])
        if not reset_data:
            current_dataset = self.__data_storage.get('traindata', ([], []))

        updated_dataset = (current_dataset[0] + new_data_set[0],
                           current_dataset[1] + new_data_set[1])

        self.__data_storage.set('traindata', updated_dataset)

        return updated_dataset
