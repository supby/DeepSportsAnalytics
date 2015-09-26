import numpy as np
import theano

# function for classifying a input vector
def classify_ann(ann, inp):
    inp = np.asarray(inp)
    inp.shape = (1, np.shape(inp)[0])
#    print ['{:.2f}'.format(float(v)) for v in ann.fprop(theano.shared(inp, name='inputs')).eval()[0]]
    return np.argmax(ann.fprop(theano.shared(inp, name='inputs')).eval())

def classify_dbm(dbm, inp):
    inp = np.asarray(inp)
    inp.shape = (1, np.shape(inp)[0])
#    print ['{:.2f}'.format(float(v)) for v in ann.fprop(theano.shared(inp, name='inputs')).eval()[0]]
    return np.argmax(dbm.mf(inp))


def score(dataset, cl_func, model, lim=None):
    nr_correct = 0
    i = 0
    for features, label in dataset:
        if lim and i == lim:
            break
        if cl_func(model, features) == np.argmax(label):
            nr_correct += 1
        i += 1
        print "row %s" % i
    total = lim if lim else len(dataset)
    print '%s/%s correct, %s%%' % (nr_correct, total, (float(nr_correct) / total) * 100)
