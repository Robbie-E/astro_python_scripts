# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 13:50:29 2020

@author: Robbie
"""

import time
from numpy import array, abs, radians, degrees, sin, cos, arcsin, sqrt, argsort, inf, searchsorted

def angular_dist(alpha1, delta1, alpha2, delta2):
  #input and output in radians
  a = sin(0.5*abs(delta1 - delta2))**2
  b = cos(delta1)*cos(delta2)*sin(0.5*abs(alpha1 - alpha2))**2
  return 2*arcsin(sqrt(a + b))

def crossmatch(cat1, cat2, max_dist):
  """
  loop cat2 sorted by delta2, break when delta-R => delta2 => delta1+R,
  use binary search when to start and end search,
  trig conversion occurs only once, before any distance calculations,
  vectorized calculation of distances (less for loops),
  max_dist in degrees, cats in degrees
  cat1 is target (bss) cat2 is super
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

    dist = inf
    closest_obj2_ind = 0
    #sort cat2 by increasing delta2, i.e. cat2[cat2[:,1].argsort()] or cat2[argsort(cat2, axis=0)[:,1]]
    #cat2_ids_sorted is an array of ids in cat2 in order of increasing delta2
    cat2_ids_sorted = argsort(cat2, axis=0)[:,1]
    obj2_alphas = cat2[cat2_ids_sorted][:,0]
    obj2_deltas = cat2[cat2_ids_sorted][:,1]
    
    #seach only within delta1-R <= delta2 <= delta1+R
    #find start and end index using binary search
    start_id = searchsorted(obj2_deltas, obj1_delta-max_dist, side='left')
    end_id = searchsorted(obj2_deltas, obj1_delta+max_dist, side='right')
    for delta2_id in range(start_id,end_id):
      obj2_alpha = obj2_alphas[delta2_id]
      obj2_delta = obj2_deltas[delta2_id]
      obj_dist = angular_dist(obj1_alpha, obj1_delta, obj2_alpha, obj2_delta)
      if obj_dist < dist:
        dist = obj_dist
        closest_obj2_ind = cat2_ids_sorted[delta2_id]
        
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
