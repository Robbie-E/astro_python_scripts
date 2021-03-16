# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 00:11:39 2020

@author: Robbie
"""

from astropy.io import fits
from numpy import zeros
import matplotlib.pyplot as plt

#mean of a set of FITS files
def mean_fits(fitfilelist):
  samp = fits.open(fitfilelist[0])[0].data
  mean_array = zeros((int(samp.shape[0]),int(samp.shape[1])))
  for fitfile in fitfilelist:
    hdulist = fits.open(fitfile)
    mean_array += hdulist[0].data
  mean_array = mean_array/float(len(fitfilelist))
  return mean_array

if __name__ == '__main__':
  
  # Test your function with examples from the question
  data  = mean_fits(['image0.fits', 'image1.fits', 'image2.fits', 'image3.fits', 'image4.fits'])
  print(data[100, 100])

  # You can also plot the result:
  plt.imshow(data.T, cmap=plt.cm.viridis)
  plt.colorbar()
  plt.show()
