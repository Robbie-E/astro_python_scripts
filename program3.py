# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 00:08:25 2020

@author: Robbie
"""

# Read (load) a FITS file
from astropy.io import fits
from numpy import argmax, unravel_index
import matplotlib.pyplot as plt

def load_fits(fitfile):
  """
  finds the position of brightest pixel
  """
  hdulist = fits.open(fitfile)
  data = hdulist[0].data
  return unravel_index(argmax(data, axis=None), data.shape)

if __name__ == '__main__':
  # Run your `load_fits` function with examples:
  bright = load_fits('image1.fits')
  print(bright)

  # You can also confirm your result visually:
  hdulist = fits.open('image1.fits')
  data = hdulist[0].data

  # Plot the 2D image data
  plt.imshow(data.T, cmap=plt.cm.viridis)
  plt.colorbar()
  plt.show()
