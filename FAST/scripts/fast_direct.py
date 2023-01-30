# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 12:14:18 2021

@author: kschroder
"""

def fast_direct(udf_fname,lookup_dir,results_dir,flood_rasters):
    import sys,os
    
    # Need to add hazpy folder to path to load it, if not installed with conda/pip
    #hazpy_dir = r'C:\Users\kxs4239\Anaconda3\envs\geo_env\Lib\site-packages\hazpy'
    #sys.path.insert(0,hazpy_dir)
    from hazpy.flood import UDF
    
    import seaborn as sns
    
    # requires utm package which isn't very standard, conda install -c conda-forge utm
    # pyodbc as well, conda install -c anaconda pyodbc
    # sqlalchemy also, conda install sqlalchemy
    
    #also install xhtml2pdf
    
    #%%
    # copied after gui_program.py, https://github.com/nhrap-hazus/FAST/blob/main/Python_env/gui_program.py
    # update the values (right side of :) with column names used in your UDF
    fields = {'UserDefinedFltyId':'FltyId',
                 'OCC':'Occ',
                 'Cost':'Cost',
                 'Area':'Area',
                 'NumStories':'NumStories',
                 'FoundationType':'FoundationType',
                 'FirstFloorHt':'FirstFloorHt',
                 'ContentCost':'ContentCost',
                 'BDDF_ID':'',
                 'CDDF_ID':'',
                 'IDDF_ID':'',
                 'InvCost':'',
                 'SOID':'', # 'Specific Occupancy ID'
                 'Latitude':'Latitude',
                 'Longitude':'Longitude',
                 'flC':'', # Coastal Flooding attribute (flC)
                 }
    
    # List of column names for Hazus names/capitalization
    fmap = [value for key,value in fields.items()]
    #%% Define inputs
    # FAST_dir = r'C:\Users\klauspc\Desktop\2021\research\FAST'
    # os.chdir(FAST_dir)
    
    # udf_fname = os.path.join(FAST_dir,'UDF','only_mdelrey_xypointdata_finalupdated.csv')
    # lookup_dir = os.path.join(FAST_dir,'Lookuptables')
    # results_dir = os.path.join(FAST_dir,'results') # we can change this name for different scenarios, or collect all outputs for analysis later
    
    # flood_depth_fname = os.path.join(FAST_dir,'rasters','wd_noaction_tideonly_slr175_ft.tif')
    
    
    
    # if not os.path.isdir(results_dir):
    #     os.makedirs(results_dir)
    
    #
    #%% Run UDF
    for flood_raster in flood_rasters[:]: # loop through scenario pairs using main domain as identifier #change after the : to change number of runs
        in_dict = {'UDFOrig':udf_fname,
                   'LUT_Dir':lookup_dir,
                   'ResultsDir':results_dir,
                   'DepthGrids':[flood_raster], # must be a list, can use more than one grid
                   'QC_Warning':"False", # quality control - print issues
                   'fmap':fmap}
        
        runUDF = UDF()
        haz = runUDF.flood_damage(**in_dict)
        
        if not haz[0]: # haz[0] is True if successful
            print("!!!!!!!! Hazus flood damage unsuccessful !!!!!!!!")
            print(haz[1]) # print the error message
    
    
    #%%
    # fmap = UserDefinedFltyId,OccupancyClass,Cost,Area,NumStories,FoundationType,
    #        FirstFloorHt,ContentCost,BldgDamageFnID,ContDamageFnId,InvDamageFnId,
    #        InvCost,SOI,latitude,longitude,flC