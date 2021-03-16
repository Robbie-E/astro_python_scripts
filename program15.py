# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 14:00:46 2020

@author: Robbie
"""

import time
from astropy.coordinates import SkyCoord
from astropy import units as u
  
def crossmatch(cat1, cat2, max_dist):
  """
  uses k-d trees to cross-match,
  max_dist in degrees, cats in degrees,
  cat1 is target, cat2 is searched for match in cat1,
  returns id1 and id2 of matching objects and id1 without matches
  """  
  start = time.time() #time.perf_counter()
  matches = []
  no_matches = []
  cat1 = SkyCoord(cat1*u.degree, frame='icrs')
  cat2 = SkyCoord(cat2*u.degree, frame='icrs')
  """
  closest_id gives the matching object's row index in cat2,
  closest_dists gives the distance to the matching object in cat2, 
  closest_ids[obj1_id] is the obj2_id that matches obj_id1,
  closest dists.value[obj1_id] is the angular distance between obj1_id and obj2_id,
  closest_ids and closest dists.value have the same shape (N X 1) for N objs in cat1
  """
  closest_ids, closest_dists, closest_dists3d = cat1.match_to_catalog_sky(cat2)
  for obj1_id, obj2_dist in enumerate(closest_dists.value):
    if obj2_dist < max_dist:
      obj2_id = closest_ids[obj1_id]
      matches.append((obj1_id, obj2_id, obj2_dist))
    else:
      no_matches.append(obj1_id)
      
  runtime = time.time() - start #time.perf_counter() - start
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
