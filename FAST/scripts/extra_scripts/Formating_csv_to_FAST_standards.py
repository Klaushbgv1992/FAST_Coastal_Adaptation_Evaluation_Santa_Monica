#! /usr/bin python
"""
@author: KSchroder

Description:
    This python scripts reads in a dataframe via pandas, renames some columns, shorten some names
    and adds an Area column according to FAST formation needs.
"""

def input_csv_creation():
    import time
    import os, glob
    import numpy as np
    import pandas as pd
    import geopandas as gpd
    import matplotlib.pyplot as plt
    
    import rasterio
    from rasterio import mask
    from rasterio.enums import Resampling
    from rasterio.vrt import WarpedVRT
    from rasterio.io import MemoryFile
    from rasterio.crs import CRS
    
    # Read in data
    main_dir = r'C:/Users/kxs4239/Desktop/spring 2021/FAST/'
    wdir = os.path.join(main_dir,'UDF/')
    data = pd.read_csv(os.path.join(wdir, "only_mdelrey_xypointdata.csv"))
    
    # Have a look at the data
    print("headers of data ", data.head)
    
    # Shorten the names of Occupation Type
    if 'OccType' in data.columns:
        # select column occtype and change to numpy array as I prefer to work with numpy
        # This step can be probably be done with pandas itself
        occtype = data['OccType'].to_numpy()
        occtype_new = occtype.copy()
        area = np.zeros(len(occtype_new))
        for type_name in ['RES1-1SWB', 'RES1-1SNB', 'RES1-SLNB', 'RES1-3SNB', 'RES1-2SNB']:
            occtype_new[occtype == type_name] = type_name[0:4]
            print("type_name[0:4] ", type_name[0:4])
    
        for type_name in ['RES3FI', 'RES3EI', 'RES3DI', 'RES3CI', 'RES3BI', 'RES3AI']:
            occtype_new[occtype == type_name] = type_name[0:5]
            print("type_name[0:4] ", type_name[0:5])
    
        # Create an Area variable based on OccType
        area[occtype_new == 'AGR1'] = 3000
        area[occtype_new == 'COM1'] = 3000
        area[occtype_new == 'COM10'] = 5500
        area[occtype_new == 'COM2'] = 3700
        area[occtype_new == 'COM3'] = 3800
        area[occtype_new == 'COM4'] = 4600
        area[occtype_new == 'COM5'] = 5000
        area[occtype_new == 'COM6'] = 5000
        area[occtype_new == 'COM7'] = 3000
        area[occtype_new == 'COM8'] = 2900
        area[occtype_new == 'COM9'] = 7000
        area[occtype_new == 'EDU1'] = 2700
        area[occtype_new == 'EDU2'] = 9200
        area[occtype_new == 'GOV1'] = 3300
        area[occtype_new == 'GOV2'] = 5000
        area[occtype_new == 'IND1'] = 2200
        area[occtype_new == 'IND2'] = 3700
        area[occtype_new == 'IND3'] = 4900
        area[occtype_new == 'IND4'] = 4900
        area[occtype_new == 'IND5'] = 4900
        area[occtype_new == 'IND6'] = 4900
        area[occtype_new == 'REL1'] = 6300
        area[occtype_new == 'RES1'] = 1500
        area[occtype_new == 'RES2'] = 1000
        area[occtype_new == 'RES3A'] = 2700
        area[occtype_new == 'RES3B'] = 5400
        area[occtype_new == 'RES3C'] = 7300
        area[occtype_new == 'RES3D'] = 10000
        area[occtype_new == 'RES3E'] = 31000
        area[occtype_new == 'RES3F'] = 50000
        area[occtype_new == 'RES4'] = 9300
        area[occtype_new == 'RES5'] = 30000
        area[occtype_new == 'RES6'] = 20000
    
    # Reassign Foundation type to numbers instead of strings
    if 'Found_Type' in data.columns:
        foundtype = data['Found_Type'].to_numpy()
        foundtype_new = foundtype.copy()
        types = ['Pile', ' Pier', 'Solid Wall', 'Basement', 'Crawl', 'Fill', 'Slab']
        for typ1 in range(0, 7):
            foundtype_new[foundtype == types[typ1]] = typ1 + 1
    
    # Rename all the columns to what it needs to be
    data.columns = ['FltyId', 'St_Name', 'CBFips', 'DamCat', 'Occ', 'NumStories', 'Basement', 'BldgType',
                    'FirstFloorHt', 'Cost', 'ContentCost', 'Val_Other', 'Val_Vehic', 'MedYrBlt',
                    'FipsEntry', 'FoundationType', 'PostFirm', 'Teachers', 'Students', 'SchoolName',
                    'Pop2pmU65', 'Pop2pmO65', 'Pop2amU65', 'Pop2amO65', 'Longitude', 'Latitude']
    
    # Add the newly created variables foundation type and occupation type back into the dataframe
    data['Occ'] = occtype_new
    data['FoundationType'] = foundtype_new
    data.insert(5, 'Area', area)
    
    # check output before writing new file
    print("headers of data ", data.columns)
    
    # Write out to CSV file
    data.to_csv("C:/Users/kxs4239/Desktop/spring 2021/FAST/UDF/only_mdelrey_xypointdata_finalupdated.csv", index=False)
