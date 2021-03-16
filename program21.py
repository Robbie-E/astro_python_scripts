# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 02:50:39 2020

@author: Robbie
"""

from sklearn.tree import DecisionTreeRegressor
from numpy import load, zeros

def get_features_targets(data_in):
  #data_in is loaded
  """
  splits the training data into input features and corresponding targets,
  inputs are 4 colour indices and  targets are the corresponding redshifts
  """
  features = zeros((data_in.shape[0], 4))
  features[:, 0] = data_in['u'] - data_in['g']
  features[:, 1] = data_in['g'] - data_in['r']
  features[:, 2] = data_in['r'] - data_in['i']
  features[:, 3] = data_in['i'] - data_in['z']
  return features, data_in['redshift']

"""
train a decision tree and then make a prediction
"""
# load the data and generate the features and targets
data = load('sdss_galaxy_colors.npy')
features, targets = get_features_targets(data)  
# initialize model
dtr = DecisionTreeRegressor()
# train the model
dtr.fit(features, targets)
# make predictions using the same features
predictions = dtr.predict(features)
# print out the first 4 predicted redshifts
print(predictions[:4])