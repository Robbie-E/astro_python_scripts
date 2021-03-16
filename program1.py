# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 00:01:30 2020

@author: Robbie
"""

# Mean, median of a 1D array
from numpy import loadtxt, mean, median
def calc_stats(infile):
  data = loadtxt(infile, delimiter=',')
  return (round(mean(data),1), round(median(data),1))  

# You can use this to test your function.
# Any code inside this `if` statement will be ignored by the automarker.
if __name__ == '__main__':
  # Run your `calc_stats` function with examples:
  mean_csv = calc_stats('data.csv')
  print(mean_csv)