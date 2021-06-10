"""
Convert ARCv2.0 rainfall estimates from binary to netCDF format.

This script converts ARCv2.0 binary files into netCDF format (this
allow for easier data extraction in the next step).
"""

import os
import numpy as np
import xarray as xr
import subprocess
from glob import glob
from datetime import datetime as dt
import config


def read_arc(filename):
    """Read binary file and store as numpy array.

    Parameters
    ----------
    filename : str
        ARC filename.

    Returns
    -------
    array
        Numpy array of ARC rainfall field.

    """
    nx = 751
    ny = 801
    with open(filename, 'rb') as f:
        data = np.fromfile(f, dtype='>f4', count=nx * ny)
        array = np.reshape(data, [nx, ny], order='F')
        if any(n < 0 for n in array.flatten().tolist()):
            array[:, :] = -9999.0
    
    return(np.flipud(np.rot90(array)))


def get_nc_filename(filename, ncdir):
    """Determine output netCDF filename.

    Parameters
    ----------
    filename : str
        ARC filename.
    ncdir : type
        Root directory of netcdf files.

    Returns
    -------
    str
        Name of output netCDF file.

    """
    # Get filename
    bin_fname = os.path.basename(filename)
    date = bin_fname[15:23]
    
    #  Determine netCDF filename
    nc_fname = 'arc2.0_' + date + '_0.10.nc'
    nc_fname = os.path.join(ncdir, date[0:4], date[4:6], nc_fname)
    
    return(nc_fname)


def create_netCDF(rfe_arr, end_date, start_date, filename):
    """Short summary.

    Parameters
    ----------
    rfe_arr : arr
        2D array.
    end_date : str
        End date of rainfall estimate (format: YYYY-MM-DD).
    start_date : str
        Start date of the rainfall estimate (format: YYYY-MM-DD).
    filename : str
        Name of output netCDF file.

    Returns
    -------
    NetCDF file
        A netCDF file.

    """
    # Determine time value
    daterange = end_date - start_date
    
    # Define coordinates
    if len(rfe_arr.shape) == 2:
        timeval = [daterange.days]
    elif len(rfe_arr.shape) == 3:
        timeval = range(0, daterange.days + 1)
    else:
        print('Warning: Data array has neither 2 or 3 dimensions!')
    
    coords = {'lon': ('lon', np.linspace(-20, 55, 751), {'units': 'degrees_east', 'standard_name': 'longitude', 'long_name': 'longitude', 'axis': 'X'}),
              'lat': ('lat', np.linspace(-40, 40, 801), {'units': 'degrees_north', 'standard_name': 'latitude', 'long_name': 'latitude', 'axis': 'Y'}),
              'time': ('time', timeval, {'units': 'days since ' + dt.strftime(start_date, '%Y-%m-%d') + ' 0:0:0', 'long_name': 'time', 'day_begins': '06:00', 'calendar': 'standard', 'axis': 'T'})
              }
    
    # If 2D array, convert to 3D array
    if len(rfe_arr.shape) == 2:
        rfe_arr = rfe_arr.reshape(1, 801, 751)
    
    # Create xarray DataArray for rfe
    da_rfe = xr.DataArray(rfe_arr, coords=coords, dims=['time', 'lat', 'lon'])
    DS = da_rfe.to_dataset(name='rfe')
    
    # Encoding
    DS.lon.encoding = {'dtype': 'float', 'zlib': True, 'complevel': 9, '_FillValue': None}
    DS.lat.encoding = {'dtype': 'float', 'zlib': True, 'complevel': 9, '_FillValue': None}
    DS.time.encoding = {'dtype': 'int32', 'zlib': True, 'complevel': 9, '_FillValue': None}
    DS.rfe.encoding = {'dtype': 'float32', 'zlib': True, 'complevel': 9, '_FillValue': -9999.0, 'contiguous': False, 'fletcher32': False, 'original_shape': (rfe_arr.shape[0], 801, 751), 'shuffle': False}
    
    # Set variable attributes
    DS.rfe.attrs['units'] = 'mm'
    DS.rfe.attrs['long_name'] = "Rainfall Estimate"
    DS.rfe.attrs['short_name'] = "rfe"
    
    # Set global attributes
    DS.attrs['title'] = 'ARC Rainfall Estimate - Version 2.0'
    DS.attrs['institution'] = "NOAA"
    DS.attrs['Conventions'] = "CF-1.7"
    DS.attrs['history'] = "Converted from binary format to netCDF"
    DS.attrs['latmin'] = -40.0
    DS.attrs['latmax'] = 40.0
    DS.attrs['lonmin'] = -20.0
    DS.attrs['lonmax'] = 55.0
    DS.attrs['latres'] = 0.1
    DS.attrs['lonres'] = 0.1
    
    # Create output directory
    if not os.path.isdir(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    
    # Write to netCDF file
    DS.to_netcdf(filename, format='NETCDF4', unlimited_dims='time')
    os.chmod(filename, 484)
    print('Created file: %s' % os.path.basename(filename))


def convert_bin2nc(files_to_convert, ncdir):
    """Convert binary file to netcdf format.

    Parameters
    ----------
    files_to_convert : list
        List of binary files to convert.
    ncdir : str
        Root directory containing all binary files.
        
    Returns
    -------
    Netcdf file.
        A netCDF file.

    """
    # Loop over each file and convert to netCDF
    for file in files_to_convert:
        # Get netCDF filename
        nc_fname = get_nc_filename(file, ncdir)
        
        if not os.path.exists(nc_fname):
            # Create directory if it doesn't exist
            if not os.path.exists(ncdir):
                os.makedirs(ncdir)
            
            # Unzip file
            if file[-3:] == '.gz':
                cmd = 'gunzip %s' % file
                subprocess.call(cmd, shell=True)
                filein = file[:-3]
            else:
                filein = file
            
            # Read binary file
            arr = read_arc(filein)
            
            # Zip file
            cmd = 'gzip %s' % filein
            subprocess.call(cmd, shell=True)
            
            # Get date
            date = os.path.basename(filein)[15:23]
            date = date[0:4] + '-' + date[4:6] + '-' + date[6:8]
            date = dt.strptime(date, '%Y-%m-%d')
            
            # Create netCDF file using xarray
            create_netCDF(arr, date, date, nc_fname)


def determine_files_to_convert(bindir, ncdir):
    """Determine which files to convert from binary to netCDF format.
    
    Parameters
    ----------
    bindir : str
        Root directory containing all binary files.
    ncdir : str
        Root directory containing all binary files.
    
    Returns
    -------
    list
        List of binary files to convert.
    
    """
    # List files
    bin_filelist = glob(os.path.join(bindir, 'daily_clim.bin.????????*'))
    bin_filelist.sort()
    
    nc_filelist = glob(os.path.join(ncdir, '????', '??', 'arc2.0_????????_0.10.nc'))
    nc_filelist.sort()
    
    # Determine missing netcdf files
    bin_dates = [os.path.basename(x)[15:23] for x in bin_filelist]
    nc_dates = [os.path.basename(x)[7:15] for x in nc_filelist]
    convert_dates = list(set(bin_dates) - set(nc_dates))
    files_to_convert = [x for x in bin_filelist if os.path.basename(x)[15:23] in convert_dates]
    
    return(files_to_convert)


def convert():
    """Wrapper function to handle conversion from binary to netCDF format tasks."""
    # Determine which files to convert from binary to netCDF format
    files_to_convert = determine_files_to_convert(os.path.join(config.localdata_dir, 'bin'), os.path.join(config.localdata_dir, 'netcdf'))
    
    # Convert
    convert_bin2nc(files_to_convert, os.path.join(config.localdata_dir, 'netcdf'))


if __name__ in '__main__':
    convert()
