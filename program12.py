# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 01:56:34 2020

@author: Robbie
"""

from numpy import array, loadtxt, sign, abs, radians, degrees, sin, cos, arcsin, sqrt, argmin

def hms2dec(hour, minute, sec):
  return 15*(hour + (minute/60) + (sec/3600))
  
def dms2dec(degree, minute, sec):
  if sign(degree) == -1:
    return -1.0*(abs(degree) + (minute/60) + (sec/3600))
  else:
    return degree + (minute/60) + (sec/3600)
  
def angular_dist(alpha1, delta1, alpha2, delta2):
  """
  calculates haversine distance
  """
  #input in degrees
  alpha1 = radians(alpha1)
  alpha2 = radians(alpha2)
  delta1 = radians(delta1)
  delta2 = radians(delta2)
  a = sin(0.5*abs(delta1 - delta2))**2
  b = cos(delta1)*cos(delta2)*sin(0.5*abs(alpha1 - alpha2))**2
  return degrees(2*arcsin(sqrt(a + b)))
  
def import_bss():
  """
  import the AT20G BSS catalogue from bss.dat
  """
  bss_cat = loadtxt('bss.dat', usecols=range(1,7))
  id_coords = []
  for obj_id in range(int(bss_cat.shape[0])):
    obj = bss_cat[obj_id]
    id_coords.append((obj_id+1, hms2dec(obj[0],obj[1],obj[2]), dms2dec(obj[3],obj[4],obj[5])))
  return id_coords

def import_super():
  """
  import the SuperCOSMOS catalogue from super.csv
  """
  super_cat = loadtxt('super.csv', delimiter=',', skiprows=1, usecols=[0, 1])
  id_coords = []
  for obj_id in range(int(super_cat.shape[0])):
    obj = super_cat[obj_id]
    id_coords.append((obj_id+1, obj[0], obj[1]))
  return id_coords

def find_closest(cat, alpha, delta):
  """
  takes a catalogue and the position of a target source (right ascension and declination) 
  and finds the closest match for the target source in the catalogue,
  returns the ID of the closest object and the distance to that object
  i.e. the object id in cat of the closest obj to (alpha, delta) and its distance
  """
  #cat is the result of either import_bss() or import_super()
  objs_dist = []
  for obj_ind, obj_info in enumerate(cat):
    obj_id, obj_alpha, obj_delta = obj_info
    objs_dist.append(angular_dist(obj_alpha, obj_delta, alpha, delta))
  closest_obj_id = argmin(array(objs_dist), axis=None)+1
  return (closest_obj_id, objs_dist[closest_obj_id-1])

def crossmatch(cat1, cat2, max_dist):
  #max_dist in degrees
  #cat1 is bss cat2 is super
  """
  calls find_closest() to crossmatch two catalogues cat1 and cat2 within a maximum distance,
  returns id1 and id2 of matching objects and id1 without matches
  """
  matches = []
  no_matches = []
  for obj1_ind, obj1_info in enumerate(cat1):
    obj1_id, obj1_alpha, obj1_delta = obj1_info
    #search obj2_id in cat2 closest to this obj1_id in cat1
    obj2_id, dist = find_closest(cat2, obj1_alpha, obj1_delta)
    if dist < max_dist:
      matches.append((obj1_id, obj2_id, dist))
    else:
      no_matches.append(obj1_id)
  
  return (matches, no_matches)

# You can use this to test your function.
# Any code inside this `if` statement will be ignored by the automarker.
if __name__ == '__main__':
  bss_cat = import_bss()
  super_cat = import_super()

  # First example in the question
  max_dist = 40/3600
  matches, no_matches = crossmatch(bss_cat, super_cat, max_dist)
  print(matches[:3])
  print(no_matches[:3])
  print(len(no_matches))

  # Second example in the question
  max_dist = 5/3600
  matches, no_matches = crossmatch(bss_cat, super_cat, max_dist)
  print(matches[:3])
  print(no_matches[:3])
  print(len(no_matches))
