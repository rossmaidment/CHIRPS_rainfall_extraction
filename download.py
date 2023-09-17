"""
Download CHIRPS rainfall estimates.

This script downloads daily, global CHIRPS rainfall estimates in netCDF format.

Author: R. Maidment.
"""

import os
import numpy as np
import wget
from datetime import datetime as dt
import config

    
def get_filenames(remoteurl, daterange):
    """Constructs list of CHIRPS filenames given list of dates.
    
    Parameters
    ----------
    remoteurl : str
        URL of where CHIPRS rainfall files are accessed.
    daterange : list
        List of dates in datetime object.
    
    Returns
    -------
    List of filenames to process.
    
    """
    files_to_download = []
    for date in daterange:
        yyyy = str(date)
        files_to_download.append(os.path.join(remoteurl, 'chirps-v2.0.' + yyyy + '.days_p05.nc'))
    
    return(files_to_download)


def download_files(files_to_download, localdatadir):
    """Download CHIRPS files.
    
    Parameters
    ----------
    files_to_download : list
        List of filenames to process
    localdatadir : str
        Local path to store downloaded file.
    
    Returns
    -------
    Attempt to download file to local directory.
    
    """
    for url_file in files_to_download:
        
        # Check if local directory exists, if not, create
        if not os.path.exists(localdatadir):
            os.makedirs(localdatadir)
        
        # Only download if file does not exist locally
        os.chdir(localdatadir)
        local_file = os.path.join(localdatadir, os.path.basename(url_file))
        if not os.path.exists(local_file):
            try:
                filename = wget.download(url_file)
                print('Downloaded file: %s' % filename)
            except:
                print('Unable to download file: %s' % url_file)
        else:
            print('File already downloaded: %s' % local_file)


def determine_files_to_download(startdate, enddate):
    """Determine files to download given supplied start/end dates.
    
    Parameters
    ----------
    startdate : str
        Start date of rainfall estimate (format: YYYY-MM-DD).
    enddate : str
        End date of the rainfall estimate (format: YYYY-MM-DD).
    
    Returns
    -------
    list
        CHIRPS files to download.
    
    """
    # Determine dates to download
    startdate = dt.strptime(startdate, "%Y-%m-%d")
    enddate = dt.strptime(enddate, "%Y-%m-%d")
    daterange = np.arange(startdate.year, enddate.year + 1)
    #daterange = [startdate + td(n) for n in range(int((enddate - startdate).days))]
    
    return(daterange)


def download():
    """Wrapper function to handle download tasks."""
    # Determine files to download given supplied start/end dates.
    daterange = determine_files_to_download(config.startdate, config.enddate)
    
    # Get list of files to download
    if config.product == 'final':
        files_to_download = get_filenames(config.remoteurl_final, daterange)
    elif config.product == 'prelim':
        files_to_download = get_filenames(config.remoteurl_prelim, daterange)
    
    # Download files
    download_files(files_to_download, os.path.join(config.datadir, 'netcdf', config.product))


if __name__ in '__main__':
    download()
