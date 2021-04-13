# astro_python_scripts
test python scripts for astronomical applications

*Enhance signal from astronomical images by taking multiple images and 'averaging' them

program1.py - calc_stats (load a csv file and compute mean and median of 1D array of data)

program2.py - mean_datasets (load a list of files and take the mean 'image', i.e. of each cell, over all the files; mean of set of signals)

program3.py - load_fits (loads a FITS file and find the position of brightest pixel, and show the image)

program4.py - mean_fits (loads a set of FITS files and calculate the mean 'image')

program5.py - list_stats (calculates median and mean of a 1D array, not suing the stastistics package)

program6.py - time_stat (calculates average running time for a stat function using random data)

program7.py - median_fits (calculates median of a set of images, runtime, and the memory to store all FITS files)

program8.py - median_approx (implementation of binapprox algorithm to calculate the median of a list of numbers)

program9.py - median_approx_fits (estimate the median of each pixel from a set of FITS files, uses helper.py)

*Crossmatching two catalogues

program10.py 
             - hms2dec converts right ascension from HMS to decimal degrees (right ascension from 0 to 24 hrs angles)

             - dms2de converts declination from DMS to decimal degrees (declination from -90 to 90 degree angles)
             
             - angular_dist (calculates angular distance between any two points on the celestial sphere given RA and dec)
             
             - import_bss (imports AT20G BSS calatalogue, returns object id, int, and coordinates in degrees)
             
             - import_super (imports SuperCOSMOS catalogue, returns object id, int, and coordinates in degrees)
             
program11.py - find_closest (takes a catalogue and position of a target source; finds closest id and dist to this target source in catalogue)

program12.py - crossmatch (crossmatch BSS and SuperCOSMOS catalogues within a maximum distance; returns list of matches id1 and id2, and id1 of non-matches)

program13.py - crossmatch (optimized crossmatch function; converts to radians before any distance calculations, also returns time in s to run)

program14.py - crossmatch (vectorized calculation)

program14_1.py - crossmatch (ignore objects id2 in 2nd catalogue with declination far from the 1st catalogue object id1; search id2 from -90 to delta1+r)

program14_2.py - crossmatch (search from delta-r to delta+r; uses binary search to crossmatch)

program15.py - crossmatch (optimized implementation using k-d trees on Astropy module)

*Use decision trees (Regression) to determine the redshifts of galaxies from their photometric colours. 
*Use galaxies where accurate spectroscopic redshifts have been calculated as gold standard. 
*Assess the accuracy of the decision trees predictions
*We have provided the Sloan data in NumPy binary format (.npy) in a file called sdss_galaxy_colors.npy
*The relevant columns are u, g, r, i, z, and redshift

program21.py 
             - get_features_target (split training data into input features, i.e. u - g, g - r, r - i and i - z; and corresponding targets, i.e. redshifts)
             
             - train a decision tree using sklearn.tree and make predictions on redshift using the known features
             
program22.py 
             - median_diff (calculate median residual error of the model)
             
             - validate_model (split the dataset into 50:50 training-to-test ratio, return test median residual error)
              
program23.py - plot from SDSS data redshift vs r-i and u-g

plot_decision_tree.py - 

program24.py - accuracy by treedepth (50:50 split between training and test/validation, calculate test median residual errors for different max tree depth)

program25.py - cross_validate_model (uses k-fold cross validation, returns test median residual error for each k combinations)

program26.py - cross_validate_predictions (uses k-fold validation and return the predicted value for redshift for each galaxies; plots predicted vs actual redshifts)

program27.py 
             - split_galaxies_qsos (splits data containing both galaxies and QSOs into two arrays containing only galaxies and QSOs)
             
             - cross_validate_median_diff (calculate median difference for QSOs and galaxies, k-fold cross-validation is used)

*Classify galaxies into three types (ellipticals, spirals or galactic mergers) based on their observed properties
*Relevant features are color indices, eccentricity, adaptive moments, concentration (luminosity profile)
*We were able to improve on the accuracy of the decision tree classifier by using a selection of them in ensemble learning with a random forest.

program28.py 
             - splitdata_train_test (shuffle the data randomly and split into training and test data specified by training fraction)
             
             - generate_features_targets (features are u-g, g-r, r-i, i-z, ecc, m4_{u,g,r,i,z} and the concentrations for u, r, z filters; target is the class)
             
             - dtc_predict_actual (perform held-out validation and return the predicted and actual classes, i.e. galaxy shapes, from a decision tree classifier)
             
program29.py - rf_predict_actual (returns predicted and actual classes for galaxies using random forest 10-fold cross-validation,
               specifying the number of decision trees in the forest; also returns the accuracy and a confusion matrix from support_functions.py)
