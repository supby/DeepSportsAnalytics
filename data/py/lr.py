import numpy
import pickle
from sklearn import cross_validation
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import RidgeClassifier
from data.loader import load_train_data_csv_bin


if __name__ == '__main__':

    dataset = load_train_data_csv_bin('../nhl_2014-2015.csv')

    train_data = dataset[0]
    train_target = dataset[1]

    print 'Scaling the data.'
    min_max_scaler = preprocessing.MinMaxScaler()
    train_data = numpy.mat(min_max_scaler.fit_transform(train_data),
                           numpy.float32)

    X_train, X_test, y_train, y_test = \
        cross_validation.train_test_split(train_data, train_target, test_size=0.3, random_state=42)

    lr = LogisticRegression(penalty='l2', C=0.7)
    clf = lr.fit(X_train, y_train)

    print 'Use cross validation.'

    print clf.score(X_test, y_test)
