# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 01:39:01 2020

@author: Robbie
"""

# Write your find_closest function here
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
  #input and output in degrees
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

def find_closest(cat, alpha, delta):
  """
  takes a catalogue and the position of a target source (right ascension and declination) 
  and finds the closest match for the target source in the catalogue,
  return the ID of the closest object and the distance to that object
  """
  #cat is the result of import_bss()
  objs_dist = []
  for obj_ind, obj_info in enumerate(cat):
    obj_id, obj_alpha, obj_delta = obj_info
    objs_dist.append(angular_dist(obj_alpha, obj_delta, alpha, delta))
  closest_obj_id = argmin(array(objs_dist), axis=None)+1
  return (closest_obj_id, objs_dist[closest_obj_id-1])
    
# You can use this to test your function.
# Any code inside this `if` statement will be ignored by the automarker.
if __name__ == '__main__':
  cat = import_bss()
  
  # First example from the question
  print(find_closest(cat, 175.3, -32.5))

  # Second example in the question
  print(find_closest(cat, 32.2, 40.7))
