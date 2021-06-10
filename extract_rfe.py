"""
Extract ARCv2.0 rainfall estimates.

This script extracts area-average values for a given rectangular domain and
saves the output in CSV format.
"""


import os
import numpy as np
from datetime import datetime as dt
from datetime import timedelta as td
import xarray as xr
import pandas as pd
import config


def extract_rfe(filename, df):
    """Extract area-average rainfall estimates.
    
    Extracts the rainfall within a rectangular domain and computes the area-average
    rainfall.

    Parameters
    ----------
    filename : str
        ARCv2.0 file in netCDF format.
    df : pandas dataframe
        Dataframe storing coordinates of areas to extract. Must contain columns
        labeled 'N', 'S', 'W' and 'E' which contain the coordinates of the area(s)
        of interest.

    Returns
    -------
    pandas dataframe
        Dataframe of the input dataframe with appended columns giving the area-average
        rainfall for each location for the given day.

    """
    # Read in file
    ds = xr.open_dataset(filename)
    fname = os.path.basename(filename)
    print('Extracting from file: %s' % fname)
    ts = fname[7:15]
    
    # Add column for TAMSAT values
    dfc = df.copy()
    dfc[ts] = np.nan
    
    # Extract area-average for each grid
    value = list()
    for index, row in dfc.iterrows():
        ds_sub = ds.sel(lon=slice(row.W, row.E), lat=slice(row.S, row.N))
        value.append("{:.1f}".format(np.round(np.nanmean(ds_sub.rfe.values.squeeze()), 1)))
    
    dfc[ts] = value
    
    return dfc


def determine_files_to_extract(startdate, enddate):
    """Determine netCDF files to extract from.

    Parameters
    ----------
    startdate : str
        Start date of rainfall estimate (format: YYYY-MM-DD).
    enddate : str
        End date of the rainfall estimate (format: YYYY-MM-DD).

    Returns
    -------
    list
        List of netCDF files to extract from.

    """
    # Determine dates to download
    startdate = dt.strptime(config.startdate, "%Y-%m-%d")
    enddate = dt.strptime(config.enddate, "%Y-%m-%d")
    daterange = [startdate + td(n) for n in range(int((enddate - startdate).days))]
    
    # List netCDF files for only dates of interest
    filelist = []
    for root, dirs, files in os.walk(os.path.join(config.localdata_dir, 'netcdf')):
        for f in files:
            if dt.strptime(os.path.basename(f)[7:15], '%Y%m%d') in daterange:
                filelist.append((os.path.join(root, f)))
    
    return(filelist)


def extract():
    """Wrapper function to handle extraction tasks."""
    # Determine files to work with
    filelist = determine_files_to_extract(config.startdate, config.enddate)
    
    # Read in latlonfile
    df = pd.read_csv(config.latlon_file)
    df = df.round(4)
    
    # Extract and concatenate
    rfe = []
    for rfefile in filelist:
        dfrfe = extract_rfe(rfefile, df)
        rfe.append(dfrfe)
    
    rfe_ = []
    for r in rfe:
        rfe_.append(r.iloc[:, -1])
    
    all = pd.concat([df, pd.concat(rfe_, axis=1)], axis=1)
    
    # Create output directory if it doesn't exist
    localoutput_dir = os.path.join(config.localdata_dir, 'output')
    if not os.path.exists(localoutput_dir):
        os.makedirs(localoutput_dir)
    
    # Export to CSV file
    fname = os.path.join(localoutput_dir, 'arc2.0_' + config.startdate.replace('-', '') \
        + '-' + config.enddate.replace('-', '') + '_' + config.tag + '.csv')
    all.to_csv(fname, index=False)
    
    # Check if it's been created
    if os.path.exists(fname):
        print('--------------------------------------------------------------------------')
        print('Success! Created file: %s ' % fname)
        print('')
        print('This is a sample of the extracted daily rainfall values in this file ...')
        print(all.head())
        print('--------------------------------------------------------------------------')
    else:
        print('Warning! File not created: %s ' % fname)


if __name__ in '__main__':
    extract()
