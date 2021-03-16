# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 11:25:52 2020

@author: Robbie
"""

import time
from numpy import array, loadtxt, sign, abs, radians, degrees, sin, cos, arcsin, sqrt, argmin

def angular_dist(alpha1, delta1, alpha2, delta2):
  """
  input and output arrays in radians
  """
  a = sin(0.5*abs(delta1 - delta2))**2
  b = cos(delta1)*cos(delta2)*sin(0.5*abs(alpha1 - alpha2))**2
  return 2*arcsin(sqrt(a + b))

def crossmatch(cat1, cat2, max_dist):
  """
  trig conversion occurs only once, before any distance calculations
  vectorized calculation of distances (less for loops)
  max_dist in degrees, cats in degrees
  cat1 is bss cat2 is super
  returns id1 and id2 of matching objects and id1 without matches
  """
  start = time.perf_counter()
  max_dist = radians(max_dist)
  cat1 = radians(cat1)
  cat2 = radians(cat2)
  obj2_alpha = cat2[:, 0]
  obj2_delta = cat2[:, 1]

  matches = []
  no_matches = []
  
  for obj1_ind, obj1_info in enumerate(cat1):
    obj1_alpha, obj1_delta = obj1_info
    dists = angular_dist(obj1_alpha, obj1_delta, obj2_alpha, obj2_delta)
    closest_obj2_ind = argmin(dists)
    dist = dists[closest_obj2_ind]
    if dist < max_dist:
      matches.append((obj1_ind, closest_obj2_ind, degrees(dist)))
    else:
      no_matches.append(obj1_ind)
      
  runtime = time.perf_counter() - start
  return (matches, no_matches, runtime)



# You can use this to test your function.
# Any code inside this `if` statement will be ignored by the automarker.
if __name__ == '__main__':
  import numpy as np
  # The example in the question
  ra1, dec1 = np.radians([180, 30])
  cat2 = [[180, 32], [55, 10], [302, -44]]
  cat2 = np.radians(cat2)
  ra2s, dec2s = cat2[:,0], cat2[:,1]
  dists = angular_dist(ra1, dec1, ra2s, dec2s)
  print(np.degrees(dists))

  cat1 = np.array([[180, 30], [45, 10], [300, -45]])
  cat2 = np.array([[180, 32], [55, 10], [302, -44]])
  matches, no_matches, time_taken = crossmatch(cat1, cat2, 5)
  print('matches:', matches)
  print('unmatched:', no_matches)
  print('time taken:', time_taken)

  # A function to create a random catalogue of size n
  def create_cat(n):
    ras = np.random.uniform(0, 360, size=(n, 1))
    decs = np.random.uniform(-90, 90, size=(n, 1))
    return np.hstack((ras, decs))

  # Test your function on random inputs
  np.random.seed(0)
  cat1 = create_cat(10)
  cat2 = create_cat(20)
  matches, no_matches, time_taken = crossmatch(cat1, cat2, 5)
  print('matches:', matches)
  print('unmatched:', no_matches)
  print('time taken:', time_taken)
