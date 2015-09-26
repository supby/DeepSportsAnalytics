#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "andrej"
__date__ = "$May 30, 2015 1:04:58 PM$"

from data.loader import NHLDATA
from pylearn2.models.autoencoder import Autoencoder, DenoisingAutoencoder
from pylearn2.costs.autoencoder import MeanSquaredReconstructionError
from pylearn2.corruption import BinomialCorruptor
from pylearn2.corruption import GaussianCorruptor
from pylearn2.costs import mlp as mlp_cost
from pylearn2 import termination_criteria
from pylearn2.datasets import transformer_dataset
from pylearn2.train_extensions import best_params
from pylearn2.training_algorithms import learning_rule
from pylearn2.training_algorithms import sgd
from pylearn2.training_algorithms.sgd import SGD
from pylearn2.costs.ebm_estimation import SMD
from pylearn2.models import mlp
from pylearn2 import corruption
from pylearn2.train import Train
from pylearn2.utils import serial
from pylearn2.blocks import StackedBlocks
from pylearn2.models.rbm import GaussianBinaryRBM
from sklearn.preprocessing import MinMaxScaler
from pylearn2.energy_functions.rbm_energy import GRBM_Type_1
from pylearn2.corruption import GaussianCorruptor
from pylearn2.termination_criteria import EpochCounter
from pylearn2.training_algorithms.sgd import MonitorBasedLRAdjuster
from shared import predictable_model
import pickle
import sys

_BATCH_SIZE = 43
MAX_EPOCHS_UNSUPERVISED = 30

if __name__ == "__main__":
    ds_train = NHLDATA(filename='../nhl_2014-2015.csv', scaler=MinMaxScaler(),
                    batch_size=_BATCH_SIZE)
    ds_train, ds_valid = ds_train.split(0.7)
    ds_valid, ds_test = ds_valid.split(0.7)

    if 'pre_train_l1' in sys.argv:

        print
        print 'Pre Train DAE layer 1:'
        print

        Train(dataset=ds_train,
                model=DenoisingAutoencoder(
                                    corruptor=BinomialCorruptor(corruption_level=0.3),
                                    nvis=ds_train.nr_inputs,
                                    nhid=300,
                                    tied_weights=True,
                                    act_enc='tanh',
                                    act_dec='tanh',
                                    # act_dec=None,
                                    irange=0.05,
                                ),
                algorithm=SGD(
                    learning_rate=0.05,
                    cost=MeanSquaredReconstructionError(),
                    batch_size=10,
                    monitoring_batches=10,
                    monitoring_dataset=ds_valid,
                    termination_criterion=EpochCounter(max_epochs=MAX_EPOCHS_UNSUPERVISED),
                    update_callbacks=None
                ),
                save_path='./dae_l1.pkl',
                save_freq=1
        ).main_loop()

    if 'pre_train_l2' in sys.argv:

        # pretrain dae layer 2
        print
        print 'Pre Train DAE layer 2:'
        print

        transformer = pickle.load(open('./dae_l1.pkl', 'rb'))

        Train(dataset=transformer_dataset.TransformerDataset(
                    raw=ds_train,
                    transformer=transformer
                ),
                model=Autoencoder(
                    nvis=300,
                    nhid=400,
                    tied_weights=True,
                    act_enc='tanh',
                    act_dec='tanh',
                    irange=0.05,
                ),
                algorithm=SGD(
                    learning_rate=0.05,
                    cost=MeanSquaredReconstructionError(),
                    batch_size=10,
                    monitoring_batches=10,
                    monitoring_dataset=transformer_dataset.TransformerDataset(
                                raw=ds_valid,
                                transformer=transformer
                    ),
                    termination_criterion=EpochCounter(max_epochs=MAX_EPOCHS_UNSUPERVISED),
                    update_callbacks=None
                ),
                save_path='./dae_l2.pkl',
                save_freq=1
        ).main_loop()

    if 'train_sup' in sys.argv:

        # trina supervised SoftMax
        print
        print 'Train supervised Softmax layer:'
        print

        Train(dataset=ds_train,
            model=mlp.MLP(
                batch_size=_BATCH_SIZE,
                layers=[
                        mlp.PretrainedLayer(layer_name='h1',
                                            layer_content=pickle.load(open("./dae_l1.pkl", 'rb'))),
                        mlp.PretrainedLayer(layer_name='h2',
                                            layer_content=pickle.load(open("./dae_l2.pkl", 'rb'))),
                       mlp.Sigmoid(layer_name='h4', dim=200, irange=.005, init_bias=0.),
                        mlp.Softmax(
                            max_col_norm=1.9365,
                            layer_name='y',
                            n_classes=2,
                            irange=.005
                        )
                    ],
                nvis=ds_train.nr_inputs
            ),
            algorithm=SGD(
                learning_rate=.05,
                learning_rule=learning_rule.Momentum(init_momentum=.5),
                monitoring_dataset=ds_valid,
                cost=mlp_cost.Default(),
                termination_criterion=termination_criteria.MonitorBased(
                    channel_name="y_misclass",
                    prop_decrease=0.,
                    N=100
                ),
                update_callbacks=sgd.ExponentialDecay(
                    decay_factor=1.00004,
                    min_lr=.000001
                )
            ),
            extensions=[
                learning_rule.MomentumAdjustor(
                    start=1,
                    saturate=50,
                    final_momentum=.7
                ),
                best_params.MonitorBasedSaveBest('y_misclass',
                                                 '../pyl2_dae_best.pkl')
            ]
        ).main_loop()

    if 'test' in sys.argv:
        model = serial.load('../pyl2_dae_best.pkl')

        print
        print 'Accuracy of test set:'
        predictable_model.score(ds_test, model=model, cl_func=predictable_model.classify_ann)
