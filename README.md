# FAST_Coastal_Adaptation_Evaluation
This project lists the resources used to assess the efficacy of multiple coastal adaptation strategies in reducing flooding, economic damages, and impacts on the local population of Santa Monica Bay California.

The resources in this repository stem from the integration of the USGS Coastal Storm Modeling System (CoSMoS) that we modified, a numerical hydrodynamic DELFT3D flood model based on MATLAB, and FEMA's FAST flood estimation tool that we modified, based on Python. 

For more information on how we used these please refer to our paper: [An integrated approach for physical, economic, and demographic evaluation of coastal flood hazard adaptation in Santa Monica Bay, California](https://doi.org/10.3389/fmars.2022.1052373). 

Resources used should be edited according to relative locations as well as the needs of the assessment. To use this code user would need:
-> Building stock data formated according to the FAST program needs. Place data in the UDF folder.
-> User-provided flood depth data. Place data in the shapes folder
-> We masked water bodies to gain insight into the impacts of additional flood volume and flood area. If using delft3d, place wlbl and bl .mat files in the mask folder.    If using a shapefile place it in the mask_poly folder, the merge raster would need be edited accordingly. 
-> Flood depth damages Lookuptables might get updated (FEMA: Hazus flood model methodology). If so, replace them in the Lookuptables folder. 
-> User-provided census data that contain demographic information. Place it in the Census folder.
-> Digital Elevation Model (DEM) of the study area. Place it in the DEM folder.

PLEASE NOTE THAT THE THIS TOOL WAS DEVELOPED WITH FLOOD MODELING AND DAMAGE ESTIMATES RELEVANT TO THE USA. Flood depth data and flood depth damage estimations would vary for areas outside of the USA.

