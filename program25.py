# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 05:22:27 2020

@author: Robbie
"""

from numpy import zeros, median, abs
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import KFold

def get_features_targets(data_in):
  #data_in is loaded
  features = zeros((data_in.shape[0], 4))
  features[:, 0] = data_in['u'] - data_in['g']
  features[:, 1] = data_in['g'] - data_in['r']
  features[:, 2] = data_in['r'] - data_in['i']
  features[:, 3] = data_in['i'] - data_in['z']
  return features, data_in['redshift']

def median_diff(predicted, actual):
  return median(abs(predicted - actual))


def cross_validate_model(model, features, targets, k):
  kf = KFold(n_splits=k, shuffle=True)
  k_median_diffs = []
  #split the dataset in k subsets (get rows to train and test)
  for train_indices, test_indices in kf.split(features):
    train_features, test_features = features[train_indices], features[test_indices]
    train_targets, test_targets = targets[train_indices], targets[test_indices]    
    # fit the model for the current set
    model.fit(train_features, train_targets)
    # test and predict using the model
    predictions = model.predict(test_features)
    k_median_diffs.append(median_diff(predictions, test_targets))
  return k_median_diffs

if __name__ == "__main__":
  import numpy as np
  data = np.load('./sdss_galaxy_colors.npy')
  features, targets = get_features_targets(data)

  # initialize model with a maximum depth of 19
  dtr = DecisionTreeRegressor(max_depth=19)

  # call your cross validation function
  diffs = cross_validate_model(dtr, features, targets, 10)

  # Print the values
  print('Differences: {}'.format(', '.join(['{:.3f}'.format(val) for val in diffs])))
  print('Mean difference: {:.3f}'.format(np.mean(diffs)))
