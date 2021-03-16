# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 00:23:49 2020

@author: Robbie
"""

from numpy import array, mean, median

#using built-in functions
def list_stats_builtin(numlist):
  num_mean = mean(array(numlist))
  num_median = median(array(numlist))
  return (num_median, num_mean)

def list_stats(numlist):
  """
  return median and mean of a list, covers even and odd lengths
  """
  numlist.sort()
  N = len(numlist)
  mean = sum(numlist)/float(N)
  if N%2 == 0:
    median = 0.5*sum(numlist[int((0.5*N)-1):int((0.5*N)+1)])
  else:
    median = numlist[int(0.5*N)]
  return (median, mean)


# You can use this to test your function.
# Any code inside this `if` statement will be ignored by the automarker.
if __name__ == '__main__':
  # Run your function with the first example in the question.
  m = list_stats([1.3, 2.4, 20.6, 0.95, 3.1, 2.7])
  print(m)

  # Run your function with the second example in the question
  m = list_stats([1.5])
  print(m)