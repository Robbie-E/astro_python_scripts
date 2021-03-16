# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 00:46:18 2020

@author: Robbie
"""

from numpy import zeros, dstack, median
from astropy.io import fits
import time

def mean_fits(fitfilelist):
  samp = fits.open(fitfilelist[0])[0].data
  mean_array = zeros((int(samp.shape[0]),int(samp.shape[1])))
  for fitfile in fitfilelist:
    hdulist = fits.open(fitfile)
    mean_array += hdulist[0].data
  mean_array = mean_array/float(len(fitfilelist))
  return mean_array

def ave_time(func, data_in, ntrials=1):
  tot_time = 0.0
  for trial in range(ntrials):
  # modify this function to time func with ntrials times using a new random array each time
    start = time.perf_counter()
    res = func(data_in)
    runtime = time.perf_counter() - start
  # return the average run time
    tot_time += runtime
  return tot_time/float(ntrials)

def median_stack(fitfilelist):
  tup_in = tuple([fits.open(fitfile)[0].data for fitfile in fitfilelist])
  median_array = median(dstack(tup_in), axis=2)
  return median_array

def memory(fitfilelist):
  tup_in = tuple([fits.open(fitfile)[0].data for fitfile in fitfilelist])
  fit_im = dstack(tup_in)
  return fit_im.nbytes/float(1024)

def median_fits(fitfilelist):
  """ 
  returns tuple of the median, the runtime, 
  memory (in kB) to store all the FITS files in the NumPy array in memory
  """
  start = time.perf_counter()
  tup_in = tuple([fits.open(fitfile)[0].data for fitfile in fitfilelist])
  fit_im = dstack(tup_in)
  median_array = median(fit_im, axis=2)
  memory = fit_im.nbytes/float(1024)
  runtime = time.perf_counter() - start
  return(median_array, runtime, memory)

# You can use this to test your function.
# Any code inside this `if` statement will be ignored by the automarker.
if __name__ == '__main__':
  # Run your function with first example in the question.
  result = median_fits(['image0.fits', 'image1.fits'])
  print(result[0][100, 100], result[1], result[2])
  
  # Run your function with second example in the question.
  result = median_fits(['image{}.fits'.format(str(i)) for i in range(11)])
  print(result[0][100, 100], result[1], result[2])