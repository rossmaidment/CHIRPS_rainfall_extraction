"""
Extract CHIRPS rainfall estimates.

This script extracts area-average values for a given rectangular domain and
saves the output in CSV format.
"""


import os
import numpy as np
from datetime import datetime as dt
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
        CHIRPS file in netCDF format.
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
    
    # Extract times and create empty dataframe with columns headings as the date
    ts_list = [dt.strftime(pd.to_datetime(x).date(), '%Y-%m-%d') for x in ds.time.values]
    df_out = pd.DataFrame(index=np.arange(df.shape[0]), columns=ts_list)
    
    # Copy dataframe
    dfc = df.copy()
    
    # Extract area-average precipitation
    for index, row in dfc.iterrows():
        df_out.iloc[index] = ds.sel(longitude=slice(row.W, row.E), latitude=slice(row.S, row.N)).mean(dim=['longitude', 'latitude']).to_dataframe().precip
    
    # Merge with latlon dataframe
    #df_out = pd.concat([dfc, df_rfe], axis=1)
    
    return df_out


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
    daterange = np.arange(startdate.year, enddate.year + 1)
        
    # List netCDF files for only dates of interest
    filelist = []
    for root, dirs, files in os.walk(os.path.join(config.datadir, 'netcdf', config.product)):
        for f in files:
            if f != '.DS_Store':
                if int(os.path.basename(f)[12:16]) in daterange:
                    filelist.append((os.path.join(root, f)))
    
    filelist.sort()
    return(filelist)


def extract():
    """Wrapper function to handle extraction tasks."""
    # Determine files to work with
    filelist = determine_files_to_extract(config.startdate, config.enddate)
    
    # Read in latlonfile
    df = pd.read_csv(config.latlon_file)
    
    # Extract and concatenate
    rfe = []
    for rfefile in filelist:
        dfrfe = extract_rfe(rfefile, df)
        rfe.append(dfrfe)
    
    # Merge rainfall values into dataframe and crop to date range
    df_rfe = pd.concat(rfe, axis=1)
    daterange = [dt.strftime(x, '%Y-%m-%d') for x in pd.date_range(start=config.startdate, end=config.enddate, freq='D')]
    try:
        df_rfe = df_rfe[daterange].astype(float).round(1)
    except:
        print('Warning - not all dates found!')
    
    print('First date: %s' % df_rfe.columns[0])
    print('Last date: %s' % df_rfe.columns[-1])
    
    # Merge into single dataframe
    df_all = pd.concat([df, df_rfe], axis=1)
    
    # Create output directory if it doesn't exist
    localoutput_dir = os.path.join(config.datadir, 'output', config.product)
    if not os.path.exists(localoutput_dir):
        os.makedirs(localoutput_dir)
    
    # Export to CSV file
    fname = os.path.join(localoutput_dir, 'chirps2.0-' + config.product + '_' + config.startdate.replace('-', '') \
        + '-' + config.enddate.replace('-', '') + '_' + config.tag + '.csv')
    df_all.to_csv(fname, index=False)
    
    # Check if it's been created
    if os.path.exists(fname):
        print('--------------------------------------------------------------------------')
        print('Success! Created file: %s ' % fname)
        print('')
        print('This is a sample of the extracted daily rainfall values in this file ...')
        print(df_all.head())
        print('--------------------------------------------------------------------------')
    else:
        print('Warning! File not created: %s ' % fname)


if __name__ in '__main__':
    extract()
