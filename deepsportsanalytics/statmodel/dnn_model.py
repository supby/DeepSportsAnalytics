''' Main model which is serialized/desirialized from DB/file '''

import logging

from statmodel.model_base import ModelBase
from statmodel.dnn_model_data import DNNDATA

logger = logging.getLogger(__name__)

_BATCH_SIZE = 43
MAX_EPOCHS_UNSUPERVISED = 30

class DNNModel(ModelBase):

    def train(self, X, Y):
        data = DNNDATA(X=X, Y=Y, scaler=scaler)
        ds_train, ds_valid = data.split(0.7)
        ds_valid, ds_test = ds_valid.split(0.7)

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
                monitoring_dataset=self.__ds_valid,
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

    def predict(self, X):
        #return self.__classify_ann();
        pass

    def __classify_ann(self, ann, inp):
        inp = np.asarray(inp)
        inp.shape = (1, np.shape(inp)[0])
        return np.argmax(ann.fprop(theano.shared(inp, name='inputs')).eval())


    def __pre_train_dae_l1(self, ds_train, ds_valid):
        return Train(dataset=ds_train,
                        model=DenoisingAutoencoder(
                                            corruptor=BinomialCorruptor(corruption_level=0.3),
                                            nvis=ds_train.nr_inputs,
                                            nhid=300,
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
                            monitoring_dataset=ds_valid,
                            termination_criterion=EpochCounter(max_epochs=MAX_EPOCHS_UNSUPERVISED),
                            update_callbacks=None
                        )
                ).main_loop()

    def __pre_train_dae_l2(self, ds_train, ds_valid):
        transformer = pickle.load(open('./dae_l1.pkl', 'rb'))

        return Train(dataset=transformer_dataset.TransformerDataset(
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
                            )
                    ).main_loop()
