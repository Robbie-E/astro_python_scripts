# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 15:25:09 2020

@author: Robbie
"""

from numpy import zeros, zeros_like, median, abs
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import KFold
from matplotlib import pyplot as plt

def get_features_targets(data_in):
  # data_in is loaded
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
  # split the dataset in k subsets (get rows to train and test)
  for train_indices, test_indices in kf.split(features):
    train_features, test_features = features[train_indices], features[test_indices]
    train_targets, test_targets = targets[train_indices], targets[test_indices]    
    # fit the model for the current set
    model.fit(train_features, train_targets)
    # test and predict using the model
    predictions = model.predict(test_features)
    k_median_diffs.append(median_diff(predictions, test_targets))
  return k_median_diffs

def cross_validate_predictions(model, features, targets, k):
  kf = KFold(n_splits=k, shuffle=True)
  # predicted redshifts from each iteration
  all_predictions = zeros_like(targets)
  for train_indices, test_indices in kf.split(features):
    train_features, test_features = features[train_indices], features[test_indices]
    train_targets, test_targets = targets[train_indices], targets[test_indices]
    # fit the model for the current set
    model.fit(train_features, train_targets)   
    # test and predict using the model, maintain order of galaxies      
    all_predictions[test_indices] = model.predict(test_features)  
  return all_predictions    


if __name__ == "__main__":
  import numpy as np
  data = np.load('./sdss_galaxy_colors.npy')
  features, targets = get_features_targets(data)

  # initialize model
  dtr = DecisionTreeRegressor(max_depth=19)

  # call your cross validation function
  predictions = cross_validate_predictions(dtr, features, targets, 10)
  """
  You can use the built-in function in scikit-learn
  predictions = cross_val_predict(dtr, features, targets, cv=10)
  """
  # calculate and print the rmsd as a sanity check
  diffs = median_diff(predictions, targets)
  print('Median difference: {:.3f}'.format(diffs))

  # plot the results to see how well our model looks
  plt.scatter(targets, predictions, s=0.4)
  plt.xlim((0, targets.max()))
  plt.ylim((0, predictions.max()))
  plt.xlabel('Measured Redshift')
  plt.ylabel('Predicted Redshift')
  plt.show()