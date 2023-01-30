# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 14:10:51 2021
#this code was used to calculate the flood volume and flood area of the smaller canals study area

@author: schroderk
"""

import os, glob
import numpy as np
import pandas as pd
import geopandas as gpd
#import matplotlib.pyplot as plt
#import math

import affine
import rasterio
from rasterio import features
from rasterio import mask
from rasterio import plot
import csv
from PIL import Image
#from rasterio import mask
#from rasterio.enums import Resampling
#from rasterio.vrt import WarpedVRT
#from rasterio.io import MemoryFile
#from rasterio.crs import CRS
FAST_dir = r'C:\Users\kxs4239\Desktop\FAST'
results_dir = os.path.join(FAST_dir,'results')
shp_dir = os.path.join(FAST_dir,'shapes')
tif_dir = os.path.join(FAST_dir,'rasters')
mask_dir = os.path.join(FAST_dir,'mask')
dem_dir = os.path.join(FAST_dir,'DEM')
shp_fnames = glob.glob(os.path.join(shp_dir,'slr*.shp'))

#main_fnames = [i for i in shp_fnames if 'canal' not in i]
#main_fnames = [i for i in main_fnames if 'bed' not in i]

main_fnames = [i for i in shp_fnames]

# Requires "water level" and "water level (when dry: bed level)"
# from SLR000_W000_na scenario
#mask_fname = os.path.join(mask_dir,'slr000_w000_na.shp')

#%%

# Raster options
utm_epsg = 26911
cell_spacing= 2 # m
nodata_val = -9999 #was set to -9999
#col_name = "Val_1"
m2ft = 3.28084

#%%
# Import DEM
dem_fname = glob.glob(os.path.join(dem_dir,'*.tif'))
with rasterio.open(dem_fname[0]) as src:
    dem = src.read(1,masked=True)
    dem_ext = rasterio.plot.plotting_extent(src)
    dem_crs = src.crs
    
# Set grid information
left, right, bot, top = dem_ext

overlap_trans = affine.Affine(cell_spacing,0.0,left,0.0,-cell_spacing,top)
oheight = int(np.round((top-bot)/cell_spacing))
owidth=int(np.round((right-left)/cell_spacing))

#%%
for main_fname in main_fnames[:]: # loop through scenario pairs using main domain as identifier #change after the : to change number of runs
    scenario_name = main_fname.split('_canals_wlbl.shp')[0]
    base_name = os.path.basename(scenario_name)
    # canal_fname = '{}_canals_wlbl.shp'.format(scenario_name)

    # Load shapefiles - these should be water level if overlaying with DEM
    #main_gdf = gpd.read_file(main_fname)
    #canal_gdf = gpd.read_file(canal_fname)
    
    main_gdf = gpd.read_file(main_fname)
    
    
    # set coordinate systems
    main_gdf = main_gdf.set_crs(epsg=utm_epsg)
    #canal_gdf = canal_gdf.set_crs(epsg=utm_epsg)
    
    #import max depth from Matlab
    # main_wl = pd.read_csv(os.path.join(scenario_name+'_wl.csv'),header=None)
    # canal_wl = pd.read_csv(os.path.join(scenario_name+'_canals_wl.csv'),header=None)
    # main_gdf['wl_max'] = main_wl
    # canal_gdf['wl_max'] = canal_wl
    
    main_wl = pd.read_csv(os.path.join(scenario_name+'_canals_wl.csv'),header=None)
    main_gdf['wl_max'] = main_wl
    
    # add canal shps to main domain
    #main_gdf = pd.concat([main_gdf,canal_gdf],ignore_index=True)
    
    grid_profile = {'transform':overlap_trans,'crs':dem_crs,'height':oheight,
                    'width':owidth,'nodata':nodata_val}
            
    # Convert shapes to raster - no interpolation with this method (I don't think)
    v1 = rasterio.features.rasterize([(feature,val) for feature,val in zip(main_gdf['geometry'].values,main_gdf['wl_max'])],
                                     out_shape = [oheight,owidth],
                                     transform=overlap_trans,
                                     fill=nodata_val,
                                     all_touched=True)

    
    # Subtract DEM to get water depth at DEM resolution
    # v_depth = v1-dem
    
    # # Convert water depth from m to ft
    # v_depth = v_depth*m2ft
    # v_depth[v_depth<0] = -9999
    # v_depth[np.isnan(v_depth)] = -9999
    
    # Save tif 
    # tif_fname = os.path.join(tif_dir,'{}_ft.tif'.format(base_name))
    # with rasterio.open(tif_fname,'w',driver='GTiff',dtype=v_depth.dtype,
    #                    count=1,**grid_profile) as dst:
    #     dst.write(v_depth,indexes=1)

    #v1 = v1*m2ft
    # v1[v1<0] = -9999
    # v1[np.isnan(v1)] = -9999
    v1[v1<0] = 0
    v1[np.isnan(v1)] = 0
       

    
    tif_fname = os.path.join(tif_dir,'{}_canals_m.tif'.format(base_name))
    with rasterio.open(tif_fname,'w',driver='GTiff',dtype=v1.dtype,
                       count=1,**grid_profile) as dst:
        dst.write(v1,indexes=1)

    #volume piece  
    v2=v1*(2)*(2)  #cubc meter
    volume = np.sum(v2)






 
    from csv import writer
    list_data=[base_name, volume]
    volumecsv = os.path.join(results_dir, 'volume.csv')
      
    with open(volumecsv, 'a', newline='') as f_object:
         writer_object = writer(f_object)
         writer_object.writerow(list_data)  
         f_object.close()
        
        #area piece
              
    a1 = (v1>0).sum()
    area = a1*(2)*(2) #squared meter


        
                
    from csv import writer
    list_data=[base_name, area]
    areacsv = os.path.join(results_dir, 'area.csv')
        
    with open(areacsv, 'a', newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(list_data)  
        f_object.close()
