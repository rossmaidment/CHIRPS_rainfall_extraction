"""
Download ARCv2.0 rainfall estimates.

This script downloads ARCv2.0 rainfall estimates in binary format.
"""

import os
import wget
from datetime import datetime as dt
from datetime import timedelta as td
import config

    
def get_filenames(remoteurl, daterange):
    """Constructs list of ARCv2.0 filenames given list of dates.
    
    Parameters
    ----------
    remoteurl : str
        URL of ARCv2.0 rainfall files.
    daterange : list
        List of dates in datetime object.
    
    Returns
    -------
    List of filenames to process.
    
    """
    files_to_download = []
    for date in daterange:
        yyyy = "{:0>4}".format(date.year)
        mm = "{:0>2}".format(date.month)
        dd = "{:0>2}".format(date.day)
        files_to_download.append(os.path.join(remoteurl, 'daily_clim.bin.' + yyyy + mm + dd + '.gz'))
    
    return(files_to_download)


def download_files(files_to_download, localdata_dir):
    """Download ARCv2.0 files.
    
    Parameters
    ----------
    files_to_download : list
        List of filenames to process
    localdata_dir : str
        Local path to store downloaded file.
    
    Returns
    -------
    Attempt to download file to local directory.
    
    """
    for url_file in files_to_download:
        
        # Check if local directory exists, if not, create
        if not os.path.exists(localdata_dir):
            os.makedirs(localdata_dir)
        
        # Only download if file does not exist locally
        os.chdir(localdata_dir)
        local_file = os.path.join(localdata_dir, os.path.basename(url_file))
        if not os.path.exists(local_file):
            try:
                filename = wget.download(url_file)
                print('Downloaded file: %s' % filename)
            except:
                print('Unable to download file: %s' % url_file)


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
        ARCv2.0 files to download.
    
    """
    # Determine dates to download
    startdate = dt.strptime(startdate, "%Y-%m-%d")
    enddate = dt.strptime(enddate, "%Y-%m-%d")
    daterange = [startdate + td(n) for n in range(int((enddate - startdate).days))]
    
    return(daterange)


def download():
    """Wrapper function to handle download tasks."""
    # Determine files to download given supplied start/end dates.
    daterange = determine_files_to_download(config.startdate, config.enddate)
    
    # Get list of files to download
    files_to_download = get_filenames(config.remoteurl, daterange)
    
    # Download files
    download_files(files_to_download, os.path.join(config.localdata_dir, 'bin'))


if __name__ in '__main__':
    download()
