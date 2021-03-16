# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 00:57:46 2020

@author: Robbie
"""

from numpy import array, mean, std, histogram

def eps(max_value,bin_edge):
  if max_value == bin_edge:
    return 1e-6
  else:
    return 0.0

def median_bins(values, B):
  """
  calculate the mean, standard deviation, and the bins
  """
  #terminating condition: mu-sigma + n*w <= mu+sigma (n <= B)
  values = array(values)
  mu = mean(values)
  sigma  = std(values) 
  bin_ini = mu-sigma
  bin_edge = mu+sigma 
  if bin_ini <= values.min():
    bin_width = (2*sigma)/float(B) #(bin_edge-values.min())/float(B)
    n_intervals = int((2*sigma)/bin_width) #int((bin_edge-values.min())/bin_width)
    bin_intervals = [bin_ini+(n*bin_width) for n in range(n_intervals)]+[bin_ini+(n_intervals*bin_width)-eps(values.max(),bin_edge)] #[values.min()+(n*bin_width) for n in range(n_intervals+1)]
    excluded_cts = 0
    bin_cts = histogram(values, bins=bin_intervals, range=(min(values), bin_edge))[0]
  else:
    bin_width = (2*sigma)/float(B)
    n_intervals = int((2*sigma)/bin_width)
    bin_intervals = [float(values.min())]+[bin_ini+(n*bin_width) for n in range(n_intervals)]+[bin_ini+(n_intervals*bin_width)-eps(values.max(),bin_edge)]
    tot_bin_cts = histogram(values, bins=bin_intervals, range=(min(values), bin_edge))[0]
    excluded_cts = int(tot_bin_cts[0])
    bin_cts = tot_bin_cts[1:]
  return (mu, sigma, excluded_cts, bin_cts) #, bin_ini, bin_edge, bin_width, bin_intervals)
  
def median_approx(values, B):
  """
  calls median_bins and calculates the approximated median
  """
  values = array(values)
  N = values.size
  bin_info = median_bins(values, B)
  mu = bin_info[0]
  sigma = bin_info[1]
  bin_ini = mu-sigma
  bin_width = (2*sigma)/float(B)
  #start with counts of excluded bins
  total = bin_info[2]
  bin_cts = bin_info[3]
  median_bin = 0.0
  for bin_index in range(bin_cts.size):
    total+= bin_cts[bin_index]
    if total >= (N+1)/2:
      median_bin = bin_index
      break
  if values.max() == mu+sigma:
    return bin_ini + ((B-1)*bin_width) + (0.5*bin_width)
  else:
    return bin_ini + (median_bin*bin_width) + (0.5*bin_width)
     
  
  
# You can use this to test your functions.
# Any code inside this `if` statement will be ignored by the automarker.
if __name__ == '__main__':
  # Run your functions with the first example in the question.
  print(median_bins([1, 1, 3, 2, 2, 6], 3))
  print(median_approx([1, 1, 3, 2, 2, 6], 3))

  # Run your functions with the second example in the question.
  print(median_bins([1, 5, 7, 7, 3, 6, 1, 1], 4))
  print(median_approx([1, 5, 7, 7, 3, 6, 1, 1], 4))
  
  print(median_bins([0, 1], 5))
  print(median_approx([0, 1], 5))

  print(median_bins([1, 1, 1000], 5))
  print(median_approx([1, 1, 1000], 5))