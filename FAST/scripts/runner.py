# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 16:35:46 2021

@author: schroderk
"""
import time
import os, glob, sys
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import math
import mapclassify
#import sqlalchemy
import rasterio
from rasterio import features
import fiona
from rasterio import mask
#%%
# set directory
FAST_dir = r'C:\Users\Klaus\Desktop\FAST'
sys.path.insert(1, os.path.join(FAST_dir,'scripts'))

#%%
# merge shapefiles into a single flood raster and mask with current water levels
shp_dir = os.path.join(FAST_dir,'shapes')
mask_dir = os.path.join(FAST_dir,'mask')
mask_poly_dir = os.path.join(FAST_dir,'mask_poly')
dem_dir = os.path.join(FAST_dir,'DEM')
prepolymask_dir = os.path.join(FAST_dir,'prepolymask_rasters_m') #masked by base slr000_w000_na
maps_dir = os.path.join(FAST_dir,'rasters_m') #masked by base and pol
prepolymask_ft_dir = os.path.join(FAST_dir,'prepolymask_rasters_ft')
tif_dir = os.path.join(FAST_dir,'rasters') #in feet used by FAST


# Requires "water level (when dry: bed level)" and "bed level in water level points"
shp_fnames = glob.glob(os.path.join(shp_dir,'slr*.shp'))
main_fnames = [i for i in shp_fnames if 'canal' not in i]
main_fnames = [i for i in main_fnames if 'bed' not in i]

mask_fnames = glob.glob(os.path.join(mask_dir,'slr*.shp'))
mask_fnames = [i for i in mask_fnames if 'canal' not in i]
mask_fnames = [i for i in mask_fnames if 'bed' not in i]
 
from mergeraster import *
mergeraster(main_fnames,mask_fnames,dem_dir,prepolymask_dir,mask_poly_dir,tif_dir,maps_dir,prepolymask_ft_dir,shp_dir)

# #mergeraster(main_fnames,mask_fname,dem_dir,tif_dir)

#%%
# run FAST analysis
udf_fname = os.path.join(FAST_dir,'UDF','mdelrey.csv')
lookup_dir = os.path.join(FAST_dir,'Lookuptables')
results_dir = os.path.join(FAST_dir,'results') 

# import list of flood rasters from merge step above
flood_rasters = glob.glob(os.path.join(tif_dir,'*.tif'))

if not os.path.isdir(results_dir):
    os.makedirs(results_dir)

from fast_direct import *
fast_direct(udf_fname,lookup_dir,results_dir,flood_rasters)

#%%
# run demographic analysis
# import census shapefile once
census_path = os.path.join(FAST_dir,'census','ca_sm_censusblocks.shp') # this is the name of the smaller shp
census_df = gpd.read_file(census_path) # clip the file to your area, this might take a long time
utm_epsg = 26911
census_df = census_df.to_crs(epsg=utm_epsg)
census_df = census_df.rename(columns={"CensusBloc":"CensusBlock"})
census_df = census_df.set_index(census_df.CensusBlock.astype(np.int64))

#import demographic data by census block
hzDemographicsB = pd.read_csv(os.path.join(FAST_dir,'census','hzDemographicsB.csv'))
hzDemographicsB = hzDemographicsB.set_index('CensusBlock')
    
from demographics import *
demographics(FAST_dir,flood_rasters,census_df,hzDemographicsB)

#%% use this section if you want to plot impacts on cencus block level in 'graphs' 
# plot maps of results by Census block
# import list of demographic results in csv
# demo_fnames = glob.glob(os.path.join(FAST_dir,'results','*_demo.csv'))
# for demo_f in demo_fnames:
#     demoFlood = pd.read_csv(demo_f,index_col='CensusBlock')
#     cb_demo = census_df.join(demoFlood) #join census shapefile with demo results
#     cb_demo = cb_demo[~np.isnan(cb_demo.Population)] #remove nan
#     cb_demo = cb_demo[cb_demo.Population>0] #remove zero values
#     cb_demo.plot(column='Population',cmap='OrRd',legend=True)#,scheme='natural_breaks')

# # import list of damage results in csv
# damage_fnames = glob.glob(os.path.join(FAST_dir,'results','*_sorted.csv'))
# for damage_f in damage_fnames:
#     damageFlood = pd.read_csv(damage_f,index_col='CBFips')
#     damageFlood = damageFlood.rename_axis('CensusBlock')
#     damageFlood = damageFlood.groupby(['CensusBlock']).sum() #aggregate by Census block
#     cb_damage = census_df.join(damageFlood) #join cenesus shapefile with damage results
#     cb_damage['Unit_Total'] = cb_damage['BldgLossUSD'] + \
#                               cb_damage['InventoryLossUSD'] + \
#                               cb_damage['ContentLossUSD'] #sum all loss types
#     cb_damage = cb_damage[~np.isnan(cb_damage.Unit_Total)] #remove nan
#     cb_damage = cb_damage[cb_damage.Unit_Total>0] #remove zero values
#     cb_damage.plot(column='Unit_Total',cmap='OrRd',legend=True)#,scheme='quantiles')
    
    
#%%
# aggregate and export results
fastout_fnames=glob.glob(os.path.join(results_dir,'*_sorted.csv'))
all_total=[]

for fastout in fastout_fnames:  
    df = pd.read_csv(fastout)
    df['Unit_Total'] = df['BldgLossUSD'] + df['InventoryLossUSD']+df['ContentLossUSD']

    event_total = df['Unit_Total'].sum()
    all_total.append([event_total])

all_total=pd.DataFrame(all_total,index=fastout_fnames)
all_total.to_csv(results_dir+"eventtotal.csv")


