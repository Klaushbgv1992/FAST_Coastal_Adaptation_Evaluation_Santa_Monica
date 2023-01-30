# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 19:33:32 2021

@author: schroderk
"""
#script to analyze demographic impacts, calculated as a % of the population in each census block that gets flooded. 
#example if the census block is 10% flooded, and there are 100 low income residents in that block, 10 of them are considered to be impacted. 

def demographics(FAST_dir,flood_rasters,census_df,hzDemographicsB):
    import os, glob
    import numpy as np
    import pandas as pd
    import geopandas as gpd
    import matplotlib.pyplot as plt
    
    import rasterio
    from rasterio import features
    
    #%% uncomment this section if not using this as a def
    # Load files
    #census_path = os.path.join(FAST_dir,'census','ca_sm_censusblocks.shp') # this is the name of the smaller shp
    #census_df = gpd.read_file(census_path) # takes a long time...big file. I made smaller one for "LA county-ish"
    
    # Project to utm coordinate system
    #utm_epsg = 26911
    #census_df = census_df.to_crs(epsg=utm_epsg)
    
    #import demographic table from HAZUS and set index as Census Block
    #hzDemographicsB = pd.read_csv(os.path.join(FAST_dir,'census','hzDemographicsB.csv'))
    #hzDemographicsB = hzDemographicsB.set_index('CensusBlock')

    #%% Census block to raster
    for flood_raster in flood_rasters[:]: # loop through scenario pairs using main domain as identifier #change after the : to change number of runs
        # Unique identifier to use to later connect the raster back to the census data
        unq_id = 'OBJECTID' # this is the column that will be used to assign values to the raster, can't use blocks because numbers are too long
        nan_val = 0 # to remove cell data where no blocks occur later
        block_nums = census_df[unq_id].values
        
        with rasterio.open(flood_raster) as drast:
            
            drast_profile = drast.profile
            # Store raster as np array
            drast_array = drast.read()[0]
            #drast_array[drast_array==drast.nodata] = np.nan
            drast_array[drast_array<=0] = np.nan

            # Assign feature information to a new array
            out_vals = rasterio.features.rasterize([(feature,val) for feature,val in zip(census_df['geometry'].values,block_nums)],
                                                    out_shape=drast.shape,
                                                    transform=drast.transform,
                                                    fill=nan_val
                                                  )
            
        
        save_tif = False
        if save_tif:    
            # Can save it to a tif, or keep it a raster. To save it:
            out_block_rast = os.path.join(FAST_dir,'census_sm_blocks.tif')
            
            block_profile = drast_profile.copy()
            block_profile['compress'] = 'lzw'
            # block_profile['dtype'] = rasterio.uint32
            
            # Can set nan values before saving (for floats only..)
            out_vals = out_vals.astype('float')
            out_vals[out_vals==nan_val] = np.nan
            
            with rasterio.open(out_block_rast,'w',**block_profile) as rblock:
                rblock.write(out_vals,indexes=1)  
            
    #%% Analyze depth for each block
    
        # The out_vals array was built to be exactly the same size as the drast_array, so you can extract
        # information for each unique value in the block array 
        #hzCensusBlock = pd.read_csv(os.path.join(wdir,'hzCensusBlock.csv'))
        #hzCensusBlock = hzCensusBlock.set_index('CensusBlock')
    
        unq_vals = np.unique(out_vals)
        unq_vals = unq_vals[1:]
        
        save_data = []
        
        for unq_val in unq_vals: # loop through unique "block" values, really objectid's
            depth_hits = drast_array[out_vals == unq_val]
            # remove nans
            #depth_hits = depth_hits[~np.isnan(depth_hits)]
            if len(depth_hits)>0: # only save outputs where it intersects with the model grid
                save_data.append([unq_val,
                                  np.nanmin(depth_hits),
                                  np.nanmean(depth_hits),
                                  np.nanmedian(depth_hits),
                                  np.nanmax(depth_hits),
                                  len(depth_hits), 
                                  len(depth_hits[~np.isnan(depth_hits)]),
                                  int(census_df.loc[census_df.OBJECTID==unq_val].CensusBlock.values[0])])
        
        # Make a dataframe for the outputs
        save_cols = [unq_id,'mind','meand','medd','maxd','all_cells', "flooded_cell",'CensusBlock']
        block_stat_df = pd.DataFrame(save_data,columns=save_cols)
        #block_stat_df['CensusBlock'] = block_stat_df['CensusBlock'].astype(np.int64)
        block_stat_df=block_stat_df.set_index('CensusBlock')
        #percentage column
        block_stat_df['PercentageVal']=(block_stat_df['flooded_cell']/block_stat_df['all_cells'])
        
        save_df = False
        if save_df:
            out_dfpath = os.path.join(FAST_dir,'block_stats_210120.csv')
            block_stat_df.to_csv(out_dfpath,index=False)
                
    #%% Perform demographic analysis
    #may wish to define minor, moderate, major thresholds based on flood depth
    
        #create summary owner and renter fields
        hzDemographicsB['Owner'] = hzDemographicsB[['OwnerSingleUnits',\
                       'OwnerMultUnits','OwnerMultStructs','OnwerMHs']].sum(axis=1)
        hzDemographicsB['Renter'] = hzDemographicsB[['RenterSingleUnits',\
                       'RenterMultUnits','RenterMultStructs','RenterMHs']].sum(axis=1)
        
        #list variables of interest
        demoVars = ['Population','Households','GroupQuarters','MaleLess16','Male16to65',\
                    'MaleOver65','FemaleLess16','Female16to65','FemaleOver65','White',\
                    'Black','NativeAmerican','Asian','Hispanic','PacifiIslander',\
                    'OtherRaceOnly','IncLess10','Inc10to20','Inc20to30','Inc20to30','Inc30to40','Inc40to50',\
                    'Inc50to60','Inc60to75','Inc75to100','IncOver100','Owner','Renter']
        
        #determine demographics of flooded population
        demoFlood = hzDemographicsB[demoVars].multiply(block_stat_df.PercentageVal,axis="index")
        demoFlood.to_csv(os.path.join(FAST_dir,'results',os.path.basename(flood_raster)[:-4]+"_demo.csv"))
        
        #calculate summary values across all Census blocks
        demoFloodSum = demoFlood.sum(axis=0)
        
        demoFloodSum.to_csv(os.path.join(FAST_dir,'results',os.path.basename(flood_raster)[:-4]+"_demo.csv"))
    
    
    
    
    
    
