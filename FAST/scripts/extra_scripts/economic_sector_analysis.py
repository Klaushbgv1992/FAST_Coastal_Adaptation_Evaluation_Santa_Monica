# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 16:46:28 2022

@author: schroderk
"""

#AFTER RUNNING FAST USE THIS TO ANALIZE ECONIMIC IMPACTS ON DIFFERENT SECTORS

import pandas as pd
import os, glob, sys

FAST_dir = r'C:\Users\klaus\Desktop\FAST'
results_dir = os.path.join(FAST_dir,'results')

fastout_fnames=glob.glob(os.path.join(results_dir,'*_sorted.csv'))
all_total=[]

for fastout in fastout_fnames:  
    df = pd.read_csv(fastout)
    res_bldgloss   = df.loc[df['Occ'].isin(['RES1', 'RES2','RES3A','RES3B','RES3C','RES3D','RES3E','RES3F','RES4','RES5','RES6']), 'BldgLossUSD'].sum()
    res_invtryloss = df.loc[df['Occ'].isin(['RES1', 'RES2','RES3A','RES3B','RES3C','RES3D','RES3E','RES3F','RES4','RES5','RES6']), 'InventoryLossUSD'].sum()
    res_cntntloss  = df.loc[df['Occ'].isin(['RES1', 'RES2','RES3A','RES3B','RES3C','RES3D','RES3E','RES3F','RES4','RES5','RES6']), 'ContentLossUSD'].sum()
    res_total      = res_bldgloss + res_invtryloss + res_cntntloss
    
    com_bldgloss   = df.loc[df['Occ'].isin(['AGR1','COM1', 'COM10','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9']), 'BldgLossUSD'].sum()
    com_invtryloss = df.loc[df['Occ'].isin(['AGR1','COM1', 'COM10','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9']), 'InventoryLossUSD'].sum()
    com_cntntloss  = df.loc[df['Occ'].isin(['AGR1','COM1', 'COM10','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9']), 'ContentLossUSD'].sum()
    com_total      = com_bldgloss + com_invtryloss + com_cntntloss
    
    ind_bldgloss   = df.loc[df['Occ'].isin(['IND1', 'IND2','IND3','IND4','IND5','IND6']), 'BldgLossUSD'].sum()
    ind_invtryloss = df.loc[df['Occ'].isin(['IND1', 'IND2','IND3','IND4','IND5','IND6']), 'InventoryLossUSD'].sum()
    ind_cntntloss  = df.loc[df['Occ'].isin(['IND1', 'IND2','IND3','IND4','IND5','IND6']), 'ContentLossUSD'].sum()
    ind_total      = ind_bldgloss + ind_invtryloss + ind_cntntloss    
    
    pub_bldgloss   = df.loc[df['Occ'].isin(['REL1','EDU1', 'EDU2','GOV1','GOV2']), 'BldgLossUSD'].sum()
    pub_invtryloss = df.loc[df['Occ'].isin(['REL1','EDU1', 'EDU2','GOV1','GOV2']), 'InventoryLossUSD'].sum()
    pub_cntntloss  = df.loc[df['Occ'].isin(['REL1','EDU1', 'EDU2','GOV1','GOV2']), 'ContentLossUSD'].sum()
    pub_total      = pub_bldgloss + pub_invtryloss + pub_cntntloss
    
    combined_total = res_total + com_total + ind_total + pub_total #compared to alll_total - used as a check to make sure I captured everything
    nonres_total   = com_total + ind_total + pub_total
           
    df['Unit_Total'] = df['BldgLossUSD'] + df['InventoryLossUSD']+df['ContentLossUSD']
    event_total      = df['Unit_Total'].sum()
    all_total.append([event_total, res_total, com_total, ind_total, pub_total, nonres_total])

all_total         = pd.DataFrame(all_total,index=fastout_fnames)
all_total.columns = all_total.columns.astype(str)
all_totals2       = all_total.rename(columns={'0':'event_total', '1':'res_total', '2':'com_total', '3':'ind_total', '4':'pub_total','5':'nonres_total'})

all_totals2.to_csv(results_dir+"eventtotal.csv")
