# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 01:32:06 2020

@author: Robbie
"""

from numpy import loadtxt, sign, abs

#for bss catalog
def hms2dec(hour, minute, sec):
  return 15*(hour + (minute/60) + (sec/3600))
  
def dms2dec(degree, minute, sec):
  if sign(degree) == -1:
    return -1.0*(abs(degree) + (minute/60) + (sec/3600))
  else:
    return degree + (minute/60) + (sec/3600)
  
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

# You can use this to test your function.
# Any code inside this `if` statement will be ignored by the automarker.
if __name__ == '__main__':
  # Output of the import_bss and import_super functions
  bss_cat = import_bss()
  super_cat = import_super()
  print(bss_cat)
  print(super_cat)