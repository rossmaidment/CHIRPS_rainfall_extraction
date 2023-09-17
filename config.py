"""
Configuration file for downloading and processing CHIRPS rainfall estimates.

This is the only file users should interact with.
"""

import os

# Start and end date of period to extract rainfall (YYYY-MM-DD)
startdate = '2023-01-01'
enddate = '2023-01-15'

# Tag to assign to extracted files (e.g. 'test')
tag = 'test_2'

# Name of CSV file containing coordinates of each location
latlon_file = 'cambodia_locations.csv'

# CHIRPS product ('final' or 'prelim')
product = 'prelim'

# Specify local working directory (this is the path that contains the 'chirps_rainfall_extraction' directory)
workingdir = '/Users/rossmaidment/Documents/Work/Consultancy/Risk_Shield/chirps_rainfall_extraction'

# CHIRPS remote URL for final and prelim estimates (THIS SHOULD ONLY BE CHANGED IF THE URL CHANGES)
remoteurl_final = 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/'
remoteurl_prelim = 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/prelim/global_daily/netcdf/p05/'

#------- DO NOT CHANGE BELOW -------

# Local path where the CHIRPS rainfall files and extracted outputs will be stored
datadir = os.path.join(workingdir, 'data')

# File containing coordinates of areas to extract rainfall for. Must contain columns 'N', 'S', 'W', 'E'
latlon_file = os.path.join(workingdir, 'coordinates', latlon_file)



