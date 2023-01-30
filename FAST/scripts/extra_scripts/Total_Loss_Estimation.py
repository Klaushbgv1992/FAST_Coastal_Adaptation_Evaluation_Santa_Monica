# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 11:14:39 2021

@author: kxs4239
Description: use this to calculate a total loss after FAST results were populated. 
"""

def output_csv_creation():
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
    main_dir = r'C:/Users/kxs4239/Desktop/2021/research/FAST/'
    wdir = os.path.join(main_dir,'UDF/')
    
    file_names=glob.glob(wdir+'*_sorted.csv')
    all_total=[]
    
    for file in file_names:  
        df = pd.read_csv(file)
    
    #  print("headers of data ", df.head)
    
    #sum col 
    #col_list= list(df)
        df['Unit_Total'] = df['BldgLossUSD'] + df['InventoryLossUSD']+df['ContentLossUSD']
    
    #sum sum col 
        Event_Total = df['Unit_Total'].sum()
        all_total.append([Event_Total])
    
    all_total=pd.DataFrame(all_total,index=file_names)
    all_total.to_csv(wdir+"eventtotal.csv")
    
    #print(Event_Total)
    
    
    
    
