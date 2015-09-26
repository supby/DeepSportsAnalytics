# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "andrej"
__date__ = "$Mar 24, 2015 10:27:32 PM$"

from sklearn import preprocessing

class StandardizationScaler:
    
    def fit_transform(self, X):
        return preprocessing.scale(X)