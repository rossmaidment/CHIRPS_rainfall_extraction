"""
Wrapper file to download ARCv2.0 binary files, convert to netCDF format
and extract area-average rainfall estimates.

This script handles the following tasks:
    1. Data download
    2. Data conversion from binary to netCDF format
    3. Data extraction (area-average for rectangular domains)

Author: R. Maidment (r.i.maidment@reading.ac.uk).
"""

import download
import convert_bin2nc
import extract_rfe

# Download files
download.download()

# Convert from binary to netcdf format
convert_bin2nc.convert()

# Extract ARC rainfall estimates
extract_rfe.extract()
