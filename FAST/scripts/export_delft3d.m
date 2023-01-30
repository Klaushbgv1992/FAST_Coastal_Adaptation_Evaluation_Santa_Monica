%when using delft3d to simulate flood events this script could be used to automatically export .dat results to .mat/.shp files without
%using Quickplot
%Written by Klaus Schroder 5/24/2021

%CHANGE FILE PATHS AND SCENARIO NAMES IN THIS SECTION
%path to Quickplot matlab files
addpath('C:\Program Files (x86)\Deltares\Delft3D 4.01.00\win32\delft3d_matlab')


%path to folder containing Delft3D results
fileDir = 'E:\UTA_PhD_work\CoSMoS_outputs\storms_wrmsrt_thd_upsteam outerdomains_z0_2m\tierII_marinadelrey_final_2022_dunes_elv\SLR200_W100_NA\tierII\mk\'; 

%path for outputs (FAST shapes folder) 
outDir = 'C:\Users\Klaus\Desktop\FAST\shapes';

%specify scenario name
scenName = 'SLR200_W100_NA';

%%
%export mdelrey_hi files
d3d_qp('openfile',[fileDir '\trim-mdelrey_hi.dat'])
d3d_qp('selectfield','water level (when dry: bed level)')
d3d_qp('allt',1)
d3d_qp('exporttype','mat file (v7.3/hdf5)')
d3d_qp('exportdata',[outDir '\' scenName '_wlbl.mat'])

d3d_qp('openfile',[fileDir '\trim-mdelrey_hi.dat'])
d3d_qp('selectfield','water level (when dry: bed level)')
d3d_qp('allt',0)
d3d_qp('exporttype','ARCview shape')
d3d_qp('exportdata',[outDir '\' scenName '_wlbl.shp'])

d3d_qp('openfile',[fileDir '\trim-mdelrey_hi.dat'])
d3d_qp('selectfield','initial bed level')
d3d_qp('exporttype','mat file (v7.3/hdf5)')
d3d_qp('exportdata',[outDir '\' scenName '_bl.mat'])

%%
%export canals files
d3d_qp('openfile',[fileDir '\trim-canals.dat'])
d3d_qp('selectfield','water level (when dry: bed level)')
d3d_qp('allt',1)
d3d_qp('exporttype','mat file (v7.3/hdf5)')
d3d_qp('exportdata',[outDir '\' scenName '_canals_wlbl.mat'])

d3d_qp('openfile',[fileDir '\trim-canals.dat'])
d3d_qp('selectfield','water level (when dry: bed level)')
d3d_qp('allt',0)
d3d_qp('exporttype','ARCview shape')
d3d_qp('exportdata',[outDir '\' scenName '_canals_wlbl.shp'])

d3d_qp('openfile',[fileDir '\trim-canals.dat'])
d3d_qp('selectfield','initial bed level')
d3d_qp('exporttype','mat file (v7.3/hdf5)')
d3d_qp('exportdata',[outDir '\' scenName '_canals_bl.mat'])
d3d_qp('close')

