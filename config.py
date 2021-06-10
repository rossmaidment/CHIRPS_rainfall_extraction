"""
Configuration file for downloading and processing ARCv2.0 rainfall estimates.

This is the only file users should interact with.
"""

# Start and end date of period to extract rainfall (YYYY-MM-DD)
startdate = '2021-05-20'
enddate = '2021-06-08'

# Tag to assign to extracted files (e.g. 'test')
tag = 'run1'

# Local path where the ARCv2.0 rainfall files and extracted outputs will be stored
localdata_dir = '/gws/nopw/j04/tamsat/tamsat/scripts/user_requests/agrotosh/malawi_arc_extraction/data'

# File containing coordinates of areas to extract rainfall for. Must contain columns 'N', 'S', 'W', 'E'
latlon_file = '/gws/nopw/j04/tamsat/tamsat/data/other/user_requests/agrotosh/Malawi/Data-Request_Malawi_021120.csv'

# ARC remote URL (THIS SHOULD ONLY BE CHANGED IF THE URL CHANGES)
remoteurl = 'ftp://ftp.cpc.ncep.noaa.gov/fews/fewsdata/africa/arc2/bin'
