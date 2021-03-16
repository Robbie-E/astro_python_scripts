# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 11:14:25 2020

@author: Robbie
"""

import time
from numpy import array, loadtxt, sign, abs, radians, degrees, sin, cos, arcsin, sqrt, argmin, inf

def angular_dist(alpha1, delta1, alpha2, delta2):
  """
  input and output in radians
  """
  a = sin(0.5*abs(delta1 - delta2))**2
  b = cos(delta1)*cos(delta2)*sin(0.5*abs(alpha1 - alpha2))**2
  return 2*arcsin(sqrt(a + b))

def find_closest(cat, alpha, delta):
  #cat is the result of either import_bss() or import_super()
  #returns the object id in cat of the closest obj to (alpha, delta) and its distance
  objs_dist = []
  for obj_ind, obj_info in enumerate(cat):
    obj_alpha, obj_delta = obj_info
    objs_dist.append(angular_dist(obj_alpha, obj_delta, alpha, delta))
  closest_obj_id = argmin(array(objs_dist), axis=None)
  return (closest_obj_id, objs_dist[closest_obj_id])

def crossmatch(cat1, cat2, max_dist):
  """
  trig conversion occurs only once, before any distance calculations
  max_dist in degrees, cats in degrees
  cat1 is bss cat2 is super
  returns id1 and id2 of matching objects and id1 without matches
  """
  start = time.perf_counter()
  max_dist = radians(max_dist)
  cat1 = radians(cat1)
  cat2 = radians(cat2)
  matches = []
  no_matches = []
  
  for obj1_ind, obj1_info in enumerate(cat1):
    obj1_alpha, obj1_delta = obj1_info
    
    ##if we use find_closest
    ##search obj2_id in cat2 closest to this obj1_id in cat1
    #obj2_id, dist = find_closest(cat2, obj1_alpha, obj1_delta)
    #if dist <= max_dist:
    #  matches.append((obj1_ind, obj2_id, degrees(dist)))
    #else:
    #  no_matches.append(obj1_ind)
      
    #alternatively without using find_closest
    dist = inf
    closest_obj2_ind = 0
    for obj2_ind, obj2_info in enumerate(cat2):
      obj2_alpha, obj2_delta = obj2_info
      obj_dist = angular_dist(obj1_alpha, obj1_delta, obj2_alpha, obj2_delta)
      if obj_dist < dist:
        dist = obj_dist
        closest_obj2_ind = obj2_ind          
    if dist <= max_dist:
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