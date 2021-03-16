# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 03:03:13 2020

@author: Robbie
"""

from sklearn.tree import DecisionTreeRegressor
from numpy import zeros, median, abs

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

def median_diff(predicted, actual):
  return median(abs(predicted - actual))

def validate_model(model, features, targets):
  """
  splits the data into training and testing subsets
  trains the model and returns the prediction accuracy with median_diff
  split the data 50:50 into training and testing features and targets
  """
  split = features.shape[0]//2
  train_features = features[:split]
  train_targets = targets[:split]
  test_features = features[split:]
  test_targets = targets[split:]
  # train the model
  model.fit(train_features, train_targets)
  # test and get the predicted_redshifts
  predictions = model.predict(test_features)
  # use median_diff function to calculate the accuracy
  return median_diff(predictions, test_targets)


if __name__ == "__main__":
  import numpy as np
  data = np.load('sdss_galaxy_colors.npy')
  features, targets = get_features_targets(data)

  # initialize model
  dtr = DecisionTreeRegressor()

  # validate the model and print the med_diff
  diff = validate_model(dtr, features, targets)
  print('Median difference: {:f}'.format(diff))
