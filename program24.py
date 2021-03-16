# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 05:14:22 2020

@author: Robbie
"""

from numpy import zeros, median, abs
from matplotlib import pyplot as plt
from sklearn.tree import DecisionTreeRegressor

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


def accuracy_by_treedepth(features, targets, depths):
  # split the data into testing and training sets
  # we do a 50:50 split of training and testing data
  split = int(0.5*features.shape[0]) #features.shape[0]//2 
  train_features = features[:split]
  train_targets = targets[:split]
  test_features = features[split:]
  test_targets = targets[split:]
  # initialise arrays or lists to store the accuracies for the below loop
  train_accuracy = []
  test_accuracy = []
  # loop through depths
  for depth in depths:
    # initialize model with the maximum depth. 
    dtr = DecisionTreeRegressor(max_depth=depth)
    # train the model using the training set
    dtr.fit(train_features, train_targets)
    #compare performance between training and testing
    train_predictions = dtr.predict(train_features)
    test_predictions = dtr.predict(test_features)
    train_accuracy.append(median_diff(train_predictions, train_targets))
    test_accuracy.append(median_diff(test_predictions, test_targets))
  return train_accuracy, test_accuracy


if __name__ == "__main__":
  import numpy as np
  data = np.load('sdss_galaxy_colors.npy')
  features, targets = get_features_targets(data)

  # Generate several depths to test
  tree_depths = [i for i in range(1, 36, 2)]

  # Call the function
  train_med_diffs, test_med_diffs = accuracy_by_treedepth(features, targets, tree_depths)
  print("Depth with lowest median difference : {}".format(tree_depths[test_med_diffs.index(min(test_med_diffs))]))
    
  # Plot the results
  train_plot = plt.plot(tree_depths, train_med_diffs, label='Training set')
  test_plot = plt.plot(tree_depths, test_med_diffs, label='Validation set')
  plt.xlabel("Maximum Tree Depth")
  plt.ylabel("Median of Differences")
  plt.legend()
  plt.show()
