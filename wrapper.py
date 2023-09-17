"""
Wrapper script to download and process CHIRPS rainfall estimates

This script handles the following tasks:
    1. Data download
    3. Data extraction (area-average for rectangular domains) for multiple locations

Author: R. Maidment.
"""

import download
import extract_rfe

# Download files
download.download()

# Extract CHIRPS rainfall estimates
extract_rfe.extract()
