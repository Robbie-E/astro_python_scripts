# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 00:04:07 2020

@author: Robbie
"""

# Mean of a set of signals for each cell
from numpy import zeros, loadtxt, round
def mean_datasets(filelist):
  samp = loadtxt(filelist[0], delimiter = ',')
  mean_array = zeros((int(samp.shape[0]),int(samp.shape[1])))
  for infile in filelist:
    mean_array += loadtxt(infile, delimiter=',')
  mean_array = round(mean_array/float(len(filelist)),1)
  return mean_array

# You can use this to test your function.
# Any code inside this `if` statement will be ignored by the automarker.
if __name__ == '__main__':
  # Run your function with the first example from the question:
  print(mean_datasets(['data1.csv', 'data2.csv', 'data3.csv']))

  # Run your function with the second example from the question:
  print(mean_datasets(['data4.csv', 'data5.csv', 'data6.csv']))
