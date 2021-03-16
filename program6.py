# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 00:31:15 2020

@author: Robbie
"""

import numpy as np
import statistics
import time

def time_stat(func, size, ntrials):
  tot_time = 0.0
  for trial in range(ntrials):
  # the time to generate the random array should not be included
    data = np.random.rand(size)
    # modify this function to time func with ntrials times using a new random array each time
    start = time.perf_counter()
    res = func(data)
    runtime = time.perf_counter() - start
    # return the average run time
    tot_time += runtime
  return tot_time/float(ntrials)

def self_mean(numlist):
  N = len(numlist)
  list_mean = sum(numlist)/float(N)
  return list_mean
  
if __name__ == '__main__':
  print('{:.6f}s for self_mean'.format(time_stat(self_mean, 1000, 10**3)))
  print('{:.6f}s for np.mean'.format(time_stat(np.mean, 1000, 10**3)))  
  print('{:.6f}s for statistics.mean'.format(time_stat(statistics.mean, 1000, 10**3)))
  print('{:.6f}s for np.mean'.format(time_stat(np.mean, 1000, 10**3)))
