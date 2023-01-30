# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 16:27:39 2022

@author: SchroderK
"""
#this code calc the mean of the census blocks

import os, glob
import numpy as np
import pandas as pd
import geopandas as gpd

FAST_dir = r'C:\Users\Klaus\Desktop\FAST'

census_path = os.path.join(FAST_dir,'census','census_block_to_studyarea.shp') # this is the name of the smaller shp I created clipped to the mdelrey_hi.grd
census_df = gpd.read_file(census_path) # takes a long time...big file. I made smaller one for "LA county-ish"

mean_blockarea = census_df["BlockArea"].mean()

mean_blockarea_m = mean_blockarea*(1e+6)





