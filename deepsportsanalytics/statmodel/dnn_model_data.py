import itertools

import numpy as np
from pylearn2.datasets.dense_design_matrix import DenseDesignMatrix
from sklearn import cross_validation

class DNNDATA(DenseDesignMatrix):
    def __init__(self, X, Y, scaler,
                    split_prop=None,
                    start=0, stop=None,
                    batch_size=None):

        self._batch_size = batch_size
        if batch_size:
            stop = int(len(Y)/batch_size)*batch_size

        if not stop:
            stop = len(Y)

        X = X[start:stop]
        Y = Y[start:stop]

        if scaler:
            X = scaler.fit_transform(X)

        if split_prop:
            X1, X2, Y1, Y2 = self._split(X, Y, split_prop)
            X = X1
            Y = Y1

        super(DNNDATA, self).__init__(X=X, y=Y)

    @property
    def nr_inputs(self):
        return len(self.X[0])

    def _split(self, X, Y, prop=.8):
        return cross_validation.train_test_split(X, Y,
                                              test_size=1-prop, random_state=42)

    def split(self, prop=.8):
        X1, X2, y1, y2 = self._split(self.X, self.y, prop)
        return DNNDATA(X1, y1, batch_size=self._batch_size),\
               DNNDATA(X2, y2, batch_size=self._batch_size)

    def __len__(self):
        return self.X.shape[0]

    def __iter__(self):
        return itertools.izip_longest(self.X, self.y)
