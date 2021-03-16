# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 15:31:50 2020

@author: Robbie
"""

from numpy import zeros, mean, median, abs
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import KFold

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

def split_galaxies_qsos(data):
  """
  splits data containing both galaxies and QSOs into 
  two arrays that contain only galaxies and QSOs 
  """
  galaxy_filter = data['spec_class'] == b'GALAXY'
  galaxies = data[galaxy_filter]
  qso_filter = data['spec_class'] == b'QSO'
  qsos = data[qso_filter]
  return galaxies, qsos

def cross_validate_median_diff(data):
  features, targets = get_features_targets(data)
  dtr = DecisionTreeRegressor(max_depth=19)
  # 10-fold cross-validation using decision tree
  return mean(cross_validate_model(dtr, features, targets, 10))

if __name__ == "__main__":
    import numpy as np
    data = np.load('./sdss_galaxy_colors.npy')

    # Split the data set into galaxies and QSOs
    galaxies, qsos= split_galaxies_qsos(data)

    # Here we cross validate the model and get the cross-validated median difference
    # The cross_validated_med_diff function is in "written_functions"
    galaxy_med_diff = cross_validate_median_diff(galaxies)
    qso_med_diff = cross_validate_median_diff(qsos)

    # Print the results
    print("Median difference for Galaxies: {:.3f}".format(galaxy_med_diff))
    print("Median difference for QSOs: {:.3f}".format(qso_med_diff))
