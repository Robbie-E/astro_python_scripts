# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 15:40:13 2020

@author: Value User
"""

import numpy as np
from sklearn.tree import DecisionTreeClassifier

def splitdata_train_test(data, fraction_training):
  """
  fraction training is float between 0 and 1
  training galaxies = total galaxies*fraction
  """
  np.random.seed(0)
  np.random.shuffle(data)
  split = int(fraction_training*data.shape[0])
  train_set = data[:split]
  test_set = data[split:]
  return train_set, test_set

def generate_features_targets(data):
  """
  data contains: colors (u-g, g-r, r-i, i-z), 
  eccentricity, 4th adaptive moments (u,r,i,z),
  50% and 90% petrosian radius in u, r, z, concentration = R50/R90;
  target is the galaxy shape class
  """
  targets = data['class']
  features = np.empty(shape=(len(data), 13))
  features[:, 0] = data['u-g']
  features[:, 1] = data['g-r']
  features[:, 2] = data['r-i']
  features[:, 3] = data['i-z']
  features[:, 4] = data['ecc']
  features[:, 5] = data['m4_u']
  features[:, 6] = data['m4_g']
  features[:, 7] = data['m4_r']
  features[:, 8] = data['m4_i']
  features[:, 9] = data['m4_z']
  features[:, 10] = data['petroR50_u']/data['petroR90_u']
  features[:, 11] = data['petroR50_r']/data['petroR90_r']
  features[:, 12] = data['petroR50_z']/data['petroR90_z']
  return features, targets


def dtc_predict_actual(data):
  """
  perform a held out validation
  return the predicted and actual classes 
  """
  # split the data into training and testing sets using a training fraction of 0.7
  train, test = splitdata_train_test(data, 0.7)
  # generate the feature and targets for the training and test sets
  train_features, train_targets = generate_features_targets(train)
  test_features, test_targets = generate_features_targets(test)
  # instantiate a decision tree classifier
  model = DecisionTreeClassifier()
  # train the classifier with the train_features and train_targets
  model.fit(train_features, train_targets)
  # get predictions for the test_features
  predictions = model.predict(test_features)
  # return the predictions and the test_targets
  return predictions, test_targets


if __name__ == '__main__':
  data = np.load('galaxy_catalogue.npy')
    
  predicted_class, actual_class = dtc_predict_actual(data)

  # Print some of the initial results
  print("Some initial results...\n   predicted,  actual")
  for i in range(10):
    print("{}. {}, {}".format(i, predicted_class[i], actual_class[i]))
