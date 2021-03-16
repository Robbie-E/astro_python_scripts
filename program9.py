# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 01:06:14 2020

@author: Robbie
"""

from numpy import array, zeros, mean, std, histogram
from helper import running_stats
from astropy.io import fits
# Write your median_bins_fits and median_approx_fits here:

def median_bins_fits(fitfilelist, B):
  """
  calculate the mean, standard deviation, and the bins
  over fitfiles in fitfilelist
  """
  mus = running_stats(fitfilelist)[0]
  sigmas = running_stats(fitfilelist)[1]
  fit_dim = mus.shape
  #ex_bins is the count of pixvalues < mu-sigma 
  ex_bins = zeros(fit_dim)
  bins = zeros((fit_dim[0], fit_dim[1], B))
  bin_width = (2*sigmas)/float(B)

  ## using histogram numpy function
  #for i in range(fit_dim[0]):
  #   for j in range(fit_dim[1]):
  #      mu = mus[i,j]
  #      sigma = sigmas[i,j]
  #      bin_ini = mu-sigma
  #      bin_edge = mu+sigma
  #      width = bin_width[i,j]
  #      coord_pixvals = []  
  #      for file_index in range(len(fitfilelist)):
  #        hdulist = fits.open(fitfilelist[file_index])
  #        data = hdulist[0].data
  #        coord_pixvals.append(data[i,j])
  #      coord_pixvals = array(coord_pixvals)
  #      if coord_pixvals.min() <= bin_ini and coord_pixvals.max() > bin_edge:
  #        bin_intervals = [float(coord_pixvals.min())]+[bin_ini+(n*width) for n in range(B)]+[bin_ini+(B*width)-1e-6]
  #        tot_bins = histogram(coord_pixvals, bins=bin_intervals, range=(coord_pixvals.min(), bin_edge))[0]
  #        ex_bins[i,j] = int(tot_bins[0])
  #        bins[i,j,:] = tot_bins[1:]
  #      else:
  #        bin_intervals = [bin_ini+(n*width) for n in range(B)]+[bin_ini+(B*width)-1e-6]
  #        ex_bins[i,j] = 0
  #        bins[i,j,:] = histogram(coord_pixvals, bins=bin_intervals, range=(coord_pixvals.min(), bin_edge))[0]  
 
  for file_index in range(len(fitfilelist)):
    hdulist = fits.open(fitfilelist[file_index])
    data = hdulist[0].data
    for i in range(fit_dim[0]):
      for j in range(fit_dim[1]):
        cell_val = data[i,j]
        mu = mus[i,j]
        sigma = sigmas[i,j]
        bin_ini = mu-sigma
        bin_edge = mu+sigma
        width = bin_width[i,j]
        
        if cell_val < bin_ini:
          ex_bins[i,j] +=1
          
        if cell_val >= bin_ini and cell_val < bin_edge:
          bin_index = int((cell_val-bin_ini)/width)
          bins[i,j,bin_index] += 1
        
  return mus, sigmas, ex_bins, bins

def median_approx_fits(fitfilelist, B):
  """
  calls median_bins_fits and calculates the approximated median
  of each cell in the fits images in fitfilelist
  """
  
  N = len(fitfilelist)
  mus, sigmas, ex_bins, bins = median_bins_fits(fitfilelist, B)
  fit_dim = mus.shape
  medians = zeros(fit_dim)
  for i in range(fit_dim[0]):
    for j in range(fit_dim[1]):
      bin_ini = mus[i,j] - sigmas[i,j]
      width = (2*sigmas[i,j])/float(B)
      #include the counts of pixvals < bin_ini
      total = ex_bins[i,j]
      median_index = 0.0
      for bin_index in range(B):
        total += bins[i,j, bin_index]
        if total >= float(N+1)/2:
          median_index = bin_index
          break
      medians[i,j] = bin_ini + (median_index*width) + (0.5*width)
  return medians        

# You can use this to test your function.
# Any code inside this `if` statement will be ignored by the automarker.
if __name__ == '__main__':
  # Run your function with examples from the question.
  mean, std, left_bin, bins = median_bins_fits(['image0.fits', 'image1.fits', 'image2.fits'], 5)
  #print(bins[100, 100, :])
  median = median_approx_fits(['image0.fits', 'image1.fits', 'image2.fits'], 5)
  #print(median[100,100])