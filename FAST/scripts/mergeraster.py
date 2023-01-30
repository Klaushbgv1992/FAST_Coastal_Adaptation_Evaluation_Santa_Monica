# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 13:14:30 2021

@author: KSchroder
"""
#script to poistion, merge, mask and plot rasters from flood output csv's 
def mergeraster(main_fnames,mask_fnames,dem_dir,prepolymask_dir,mask_poly_dir,tif_dir,maps_dir,prepolymask_ft_dir,shp_dir): 
    #import time
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
    from rasterio import features
    import fiona
    from rasterio import mask
    
    #%% 

    #uncomment this section is not running it as a def
    #from rasterio import mask
    #from rasterio.enums import Resampling
    #from rasterio.vrt import WarpedVRT
    #from rasterio.io import MemoryFile
    #from rasterio.crs import CRS
    # FAST_dir = r'C:\Users\klaus\Desktop\FAST'
    # results_dir = os.path.join(FAST_dir,'results')
    # shp_dir = os.path.join(FAST_dir,'shapes')
    # tif_dir = os.path.join(FAST_dir,'rasters')
    # mask_dir = os.path.join(FAST_dir,'mask')
    # dem_dir = os.path.join(FAST_dir,'DEM')
    # shp_fnames = glob.glob(os.path.join(shp_dir,'slr*.shp'))
    # main_fnames = [i for i in shp_fnames if 'canal' not in i]
    # main_fnames = [i for i in main_fnames if 'bed' not in i]

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
    for mask_fname in mask_fnames[:]: # loop through scenario pairs using main domain as identifier #change after the : to change number of runs
        scenario_name_mask = mask_fname.split('_wlbl.shp')[0]
        base_name_mask = os.path.basename(scenario_name_mask)
        canal_fname_mask = '{}_canals_wlbl.shp'.format(scenario_name_mask)

        # Load shapefiles - these should be water level if overlaying with DEM
        main_gdf_mask = gpd.read_file(mask_fname)
        canal_gdf_mask = gpd.read_file(canal_fname_mask)
        
        # set coordinate systems
        main_gdf_mask = main_gdf_mask.set_crs(epsg=utm_epsg)
        canal_gdf_mask = canal_gdf_mask.set_crs(epsg=utm_epsg)
        
        #import max depth from Matlab
        main_wl_mask = pd.read_csv(os.path.join(scenario_name_mask+'_wl.csv'),header=None)
        canal_wl_mask = pd.read_csv(os.path.join(scenario_name_mask+'_canals_wl.csv'),header=None)
        main_gdf_mask['wl_max'] = main_wl_mask
        canal_gdf_mask['wl_max'] = canal_wl_mask
        
        # add canal shps to main domain
        main_gdf_mask = pd.concat([main_gdf_mask,canal_gdf_mask],ignore_index=True)
        
        grid_profile = {'transform':overlap_trans,'crs':dem_crs,'height':oheight,
                        'width':owidth,'nodata':nodata_val}
                
        # Convert shapes to raster - no interpolation with this method (I don't think)
        v1_mask = rasterio.features.rasterize([(feature,val) for feature,val in zip(main_gdf_mask['geometry'].values,main_gdf_mask['wl_max'])],
                                          out_shape = [oheight,owidth],
                                          transform=overlap_trans,
                                          fill=nodata_val,
                                          all_touched=True)

        
    
        #v1 = v1*m2ft #comment out if making meters rasters for maps
        # v1[v1<0] = -9999
        # v1[np.isnan(v1)] = -9999
        v1_mask = v1_mask-dem+0.792
        #v1_mask = v1_mask*m2ft
        v1_mask[v1_mask<0] = 0
        v1_mask[np.isnan(v1_mask)] = 0
        
        tif_fname = os.path.join(prepolymask_dir,'{}_m_mask.tif'.format(base_name_mask)) #also change m to ft when needed
        with rasterio.open(tif_fname,'w',driver='GTiff',dtype=v1_mask.dtype,
                            count=1,**grid_profile) as dst:
            dst.write(v1_mask,indexes=1)
    #%%
    for main_fname in main_fnames[:]: # loop through scenario pairs using main domain as identifier #change after the : to change number of runs
        scenario_name = main_fname.split('_wlbl.shp')[0]
        base_name = os.path.basename(scenario_name)
        canal_fname = '{}_canals_wlbl.shp'.format(scenario_name)

        # Load shapefiles - these should be water level if overlaying with DEM
        main_gdf = gpd.read_file(main_fname)
        canal_gdf = gpd.read_file(canal_fname)
        
        # set coordinate systems
        main_gdf = main_gdf.set_crs(epsg=utm_epsg)
        canal_gdf = canal_gdf.set_crs(epsg=utm_epsg)
        
        #import max depth from Matlab
        main_wl = pd.read_csv(os.path.join(scenario_name+'_wl.csv'),header=None)
        canal_wl = pd.read_csv(os.path.join(scenario_name+'_canals_wl.csv'),header=None)
        main_gdf['wl_max'] = main_wl
        canal_gdf['wl_max'] = canal_wl
        
        # add canal shps to main domain
        main_gdf = pd.concat([main_gdf,canal_gdf],ignore_index=True)
        
        grid_profile = {'transform':overlap_trans,'crs':dem_crs,'height':oheight,
                        'width':owidth,'nodata':nodata_val}
                
        # Convert shapes to raster - no interpolation with this method (I don't think)
        v1 = rasterio.features.rasterize([(feature,val) for feature,val in zip(main_gdf['geometry'].values,main_gdf['wl_max'])],
                                         out_shape = [oheight,owidth],
                                         transform=overlap_trans,
                                         fill=nodata_val,
                                         all_touched=True)

        
    
        #v1 = v1*m2ft #comment out if making meters rasters for maps
        # v1[v1<0] = -9999
        # v1[np.isnan(v1)] = -9999
        v1 = v1-dem+0.792
        v1[v1<0] = 0
        v1[np.isnan(v1)] = 0
        v1[v1_mask>0] = 0
        
    
        tif_fname = os.path.join(prepolymask_dir,'{}_m_masked.tif'.format(base_name)) #also change m to ft when needed
        with rasterio.open(tif_fname,'w',driver='GTiff',dtype=v1.dtype,
                           count=1,**grid_profile) as dst:
            dst.write(v1,indexes=1)
          
            
#%%
#mask with polgyon
        mask_fname = os.path.join(mask_poly_dir,'SLR000_W000_NA_MASK2.shp')

        with fiona.open(mask_fname, "r") as shapefile:
            shapes = [feature["geometry"] for feature in shapefile]

        raster_fnames = glob.glob(os.path.join(prepolymask_dir,'*.tif'))    
    
        for raster_fnames in raster_fnames[:]:
                scenario_name = raster_fnames.split('.tif')[0]
                base_name = os.path.basename(scenario_name)
    
        with rasterio.open(raster_fnames,'r') as src:
                    #out_image, out_transform = rasterio.mask.mask(src, shapes)
                    out_image, out_transform = rasterio.mask.mask(src, shapes, filled=True, nodata=0, crop=False, invert=True)
                    out_meta = src.meta
        
        out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})
        
        tif_fname = os.path.join(maps_dir,'{}_mskd_m.tif'.format(base_name))
        with rasterio.open(tif_fname, "w", **out_meta) as dest:
                dest.write(out_image)
#%%

#now for FAST rasters in feet
#mask
    for mask_fname in mask_fnames[:]: # loop through scenario pairs using main domain as identifier #change after the : to change number of runs
        scenario_name_mask = mask_fname.split('_wlbl.shp')[0]
        base_name_mask = os.path.basename(scenario_name_mask)
        canal_fname_mask = '{}_canals_wlbl.shp'.format(scenario_name_mask)

        # Load shapefiles - these should be water level if overlaying with DEM
        main_gdf_mask = gpd.read_file(mask_fname)
        canal_gdf_mask = gpd.read_file(canal_fname_mask)
        
        # set coordinate systems
        main_gdf_mask = main_gdf_mask.set_crs(epsg=utm_epsg)
        canal_gdf_mask = canal_gdf_mask.set_crs(epsg=utm_epsg)
        
        #import max depth from Matlab
        main_wl_mask = pd.read_csv(os.path.join(scenario_name_mask+'_wl.csv'),header=None)
        canal_wl_mask = pd.read_csv(os.path.join(scenario_name_mask+'_canals_wl.csv'),header=None)
        main_gdf_mask['wl_max'] = main_wl_mask
        canal_gdf_mask['wl_max'] = canal_wl_mask
        
        # add canal shps to main domain
        main_gdf_mask = pd.concat([main_gdf_mask,canal_gdf_mask],ignore_index=True)
        
        grid_profile = {'transform':overlap_trans,'crs':dem_crs,'height':oheight,
                        'width':owidth,'nodata':nodata_val}
                
        # Convert shapes to raster - no interpolation with this method (I don't think)
        v2_mask = rasterio.features.rasterize([(feature,val) for feature,val in zip(main_gdf_mask['geometry'].values,main_gdf_mask['wl_max'])],
                                          out_shape = [oheight,owidth],
                                          transform=overlap_trans,
                                          fill=nodata_val,
                                          all_touched=True)
       
    
        #v1 = v1*m2ft #comment out if making meters rasters for maps
        # v1[v1<0] = -9999
        # v1[np.isnan(v1)] = -9999
        v2_mask = v2_mask-dem+0.792
        v2_mask = v2_mask*m2ft
        v2_mask[v2_mask<0] = 0
        v2_mask[np.isnan(v2_mask)] = 0
        
        tif_fname = os.path.join(prepolymask_ft_dir,'{}_ft_mask.tif'.format(base_name_mask)) 
        with rasterio.open(tif_fname,'w',driver='GTiff',dtype=v2_mask.dtype,
                            count=1,**grid_profile) as dst:
            dst.write(v2_mask,indexes=1)
#%%base
    for main_fname in main_fnames[:]: # loop through scenario pairs using main domain as identifier #change after the : to change number of runs
        scenario_name = main_fname.split('_wlbl.shp')[0]
        base_name = os.path.basename(scenario_name)
        canal_fname = '{}_canals_wlbl.shp'.format(scenario_name)

        # Load shapefiles - these should be water level if overlaying with DEM
        main_gdf = gpd.read_file(main_fname)
        canal_gdf = gpd.read_file(canal_fname)
        
        # set coordinate systems
        main_gdf = main_gdf.set_crs(epsg=utm_epsg)
        canal_gdf = canal_gdf.set_crs(epsg=utm_epsg)
        
        #import max depth from Matlab
        main_wl = pd.read_csv(os.path.join(scenario_name+'_wl.csv'),header=None)
        canal_wl = pd.read_csv(os.path.join(scenario_name+'_canals_wl.csv'),header=None)
        main_gdf['wl_max'] = main_wl
        canal_gdf['wl_max'] = canal_wl
        
        # add canal shps to main domain
        main_gdf = pd.concat([main_gdf,canal_gdf],ignore_index=True)
        
        grid_profile = {'transform':overlap_trans,'crs':dem_crs,'height':oheight,
                        'width':owidth,'nodata':nodata_val}
                
        # Convert shapes to raster - no interpolation with this method (I don't think)
        v2 = rasterio.features.rasterize([(feature,val) for feature,val in zip(main_gdf['geometry'].values,main_gdf['wl_max'])],
                                         out_shape = [oheight,owidth],
                                         transform=overlap_trans,
                                         fill=nodata_val,
                                         all_touched=True)

        
        #comment out if making meters rasters for maps
        # v1[v1<0] = -9999
        # v1[np.isnan(v1)] = -9999
        v2 = v2-dem+0.792
        v2 = v2*m2ft
        v2[v2<0] = 0
        v2[np.isnan(v2)] = 0
        v2[v2_mask>0] = 0
        
    
        tif_fname = os.path.join(prepolymask_ft_dir,'{}_ft_masked.tif'.format(base_name))
        with rasterio.open(tif_fname,'w',driver='GTiff',dtype=v2.dtype,
                           count=1,**grid_profile) as dst:
            dst.write(v2,indexes=1)
          
            
#%%
#mask with polgyon
        mask_fname = os.path.join(mask_poly_dir,'SLR000_W000_NA_MASK2.shp')

        with fiona.open(mask_fname, "r") as shapefile:
                shapes = [feature["geometry"] for feature in shapefile]

        raster_fnames = glob.glob(os.path.join(prepolymask_ft_dir,'*.tif'))    

        for raster_fnames in raster_fnames[:]:
            scenario_name = raster_fnames.split('.tif')[0]
            base_name = os.path.basename(scenario_name)
    
        with rasterio.open(raster_fnames,'r') as src:
        #out_image, out_transform = rasterio.mask.mask(src, shapes)
                out_image, out_transform = rasterio.mask.mask(src, shapes, filled=True, nodata=0, crop=False, invert=True)
                out_meta = src.meta
       
                out_meta.update({"driver": "GTiff",
                                 "height": out_image.shape[1],
                                 "width": out_image.shape[2],
                                 "transform": out_transform})
        
        tif_fname = os.path.join(tif_dir,'{}_mskd_ft.tif'.format(base_name))
        with rasterio.open(tif_fname, "w", **out_meta) as dest:
            dest.write(out_image)

