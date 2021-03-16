# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 03:23:49 2020

@author: Robbie
"""

import numpy as np
from matplotlib import pyplot as plt

# Complete the following to make the plot
if __name__ == "__main__":
    data = np.load('sdss_galaxy_colors.npy')
    # Get a colour map
    cmap = plt.get_cmap('YlOrRd') #'hot'
    # Define our colour indexes u-g and r-i
    u_g = data['u'] - data['g']
    r_i = data['r'] - data['i']
    # Make a redshift array
    redshift = data['redshift']
    # Create the plot with plt.scatter and plt.colorbar
    color_redshift = plt.scatter(u_g, r_i, c=redshift, cmap=cmap, s=0.5, lw=0)
    bar = plt.colorbar(color_redshift)
    # Define your axis labels and plot title
    plt.title('Redshift (colour) u-g versus r-i')
    bar.set_label('Redshift')
    plt.xlabel('Colour index u-g')
    plt.ylabel('Colour index r-i')
    # Set any axis limits
    plt.xlim(-0.5,2.5)
    plt.ylim(-0.5,1.0)
    plt.show()