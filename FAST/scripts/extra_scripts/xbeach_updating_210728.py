# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 15:15:26 2021
#this code enables editing and visualization of the CoSMoS xbeach profiles 

@author: kbefus & kschroder
"""
import os
import geopandas as gpd
import numpy as np
from scipy.io import loadmat,savemat
from scipy.spatial import cKDTree as KDTree
import matplotlib.pyplot as plt
#%%

wdir = r'D:\files\xbeach'

mat_fname = os.path.join(wdir,'xbprofile2m_SLR200.mat')
mat = loadmat(mat_fname)
xbprofile = mat['xbprofile2m_SLR200'].copy().squeeze() # mat.keys() to see options for text

#%%

sw_fname = os.path.join(wdir,'current_sanberms.shp')
xsec_fname = os.path.join(wdir,'SoCA_XBchlns_fnl.shp')

sw_df = gpd.read_file(sw_fname) # can add attribute for how much to change xbeach profile
x_df = gpd.read_file(xsec_fname)

# Covert crs to cross section crs
sw_df.to_crs(x_df.crs,inplace=True)

# Adapt feature as a single polygon - otherwise have to loop
adapt_feat = sw_df.unary_union

# Only use x-secs that intersect the adaptation feature
x_df2 = x_df[x_df.intersects(adapt_feat)].copy()

# Reality check plot
fig,ax = plt.subplots()
sw_df.plot(ax=ax)
x_df2.plot(ax=ax,color='r')
#%%
plt.close('all')
add_value = None # amount to increase elevation by
elev_value = 7.572 # constant elevation to set for cells
width_inds = 6 # how wide the feature is in number of cells; difference between cells are +-1.635 and one grid cell in the hi grids is 10m wide
for ind,irow in x_df2.iterrows():
    line_id = irow['Ln_ID']-1 # to python 0-based index
    temp_geom = irow.geometry
    intersect_pt = np.array(temp_geom.intersection(adapt_feat).xy).T[0]
    
    start_pt = np.array(temp_geom.xy).T[0]
    
    # Distance in meters from start of transect
    # intersect_dist = np.sqrt((intersect_pt[0]-start_pt[0])**2 + \
    #                          (intersect_pt[1]-start_pt[1])**2)
    
    tree = KDTree(np.c_[xbprofile[line_id]['x'],
                        xbprofile[line_id]['y']])
    loc_vals = []
    dist,near_ind = tree.query(intersect_pt[None,:])
    near_ind = near_ind[0]
    
    # Use index to replace elevation
    new_z = xbprofile[line_id]['z'].copy()
    if add_value is not None:
        # To add values
        new_z[near_ind-width_inds:near_ind+width_inds+1] += add_value # add to existing elevation
    
    if elev_value is not None:
        # To set elevation
        new_z[near_ind-width_inds:near_ind+width_inds+1] = elev_value
    
    # sanity check
    fig,ax = plt.subplots()
    ax.plot(xbprofile[line_id]['x'],
            xbprofile[line_id]['z'],'k-o',label='Original {}'.format(line_id+1))
    ax.plot(xbprofile[line_id]['x'],
            new_z,'r-o',label='New {}'.format(line_id+1))
    ax.legend()
    
    # to save back into the dataset, need to overwrite profile
    xbprofile[line_id]['z'] = new_z.copy()
    
#%% Save back into new mat file
scenario_name = os.path.basename(mat_fname).split('.')[0]
adapt_name = 'current_sanberms{}m'.format(elev_value)
new_mfile = os.path.join(wdir,'{}_adapted_{}.mat'.format(scenario_name,adapt_name))
new_mat = mat.copy()
new_mat['xbprofile2m_SLR200'] = xbprofile[None,:].copy()

savemat(new_mfile,new_mat,do_compression=True,appendmat=False)
