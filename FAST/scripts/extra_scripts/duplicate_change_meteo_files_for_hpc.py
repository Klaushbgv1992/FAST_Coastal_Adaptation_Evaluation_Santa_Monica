# -*- coding: utf-8 -*-
"""
Created on Tue May 31 13:56:50 2022

@author: klaus
"""
#copy file and change name of meteofiles as needed for HPC, each domain should have its own meteo_name
import shutil
import os
#set directory
meteo_dir = r'D:\run_outputs\Setup files\tier2\runtime_extraday\Storm Scenarios with warmstarts HAVING THD upstream_z0_ 2m in outerdomains\SLR200_W100_SW\tierII\mk'

#AMP
#1
src = os.path.join(meteo_dir,'meteo.amp') 
dst = os.path.join(meteo_dir,'meteo_mdelrey_hi.amp')

shutil.copyfile(src, dst)

#2
src = os.path.join(meteo_dir,'meteo.amp') 
dst = os.path.join(meteo_dir,'meteo_mdelrey_outer.amp')

shutil.copyfile(src, dst)

#3
src = os.path.join(meteo_dir,'meteo.amp') 
dst = os.path.join(meteo_dir,'meteo_canals.amp')

shutil.copyfile(src, dst)

#4
src = os.path.join(meteo_dir,'meteo.amp') 
dst = os.path.join(meteo_dir,'meteo_socal_mk.amp')

shutil.copyfile(src, dst)

#5
src = os.path.join(meteo_dir,'meteo.amp') 
dst = os.path.join(meteo_dir,'meteo_king_hi.amp')

shutil.copyfile(src, dst)

#6
src = os.path.join(meteo_dir,'meteo.amp') 
dst = os.path.join(meteo_dir,'meteo_king_outer.amp')

shutil.copyfile(src, dst)

#AMU
#1
src = os.path.join(meteo_dir,'meteo.amu') 
dst = os.path.join(meteo_dir,'meteo_mdelrey_hi.amu')

shutil.copyfile(src, dst)

#2
src = os.path.join(meteo_dir,'meteo.amu') 
dst = os.path.join(meteo_dir,'meteo_mdelrey_outer.amu')

shutil.copyfile(src, dst)

#3
src = os.path.join(meteo_dir,'meteo.amu') 
dst = os.path.join(meteo_dir,'meteo_canals.amu')

shutil.copyfile(src, dst)

#4
src = os.path.join(meteo_dir,'meteo.amu') 
dst = os.path.join(meteo_dir,'meteo_socal_mk.amu')

shutil.copyfile(src, dst)

#5
src = os.path.join(meteo_dir,'meteo.amu') 
dst = os.path.join(meteo_dir,'meteo_king_hi.amu')

shutil.copyfile(src, dst)

#6
src = os.path.join(meteo_dir,'meteo.amu') 
dst = os.path.join(meteo_dir,'meteo_king_outer.amu')

shutil.copyfile(src, dst)

#AMV
#1
src = os.path.join(meteo_dir,'meteo.amv') 
dst = os.path.join(meteo_dir,'meteo_mdelrey_hi.amv')

shutil.copyfile(src, dst)

#2
src = os.path.join(meteo_dir,'meteo.amv') 
dst = os.path.join(meteo_dir,'meteo_mdelrey_outer.amv')

shutil.copyfile(src, dst)

#3
src = os.path.join(meteo_dir,'meteo.amv') 
dst = os.path.join(meteo_dir,'meteo_canals.amv')

shutil.copyfile(src, dst)

#4
src = os.path.join(meteo_dir,'meteo.amv') 
dst = os.path.join(meteo_dir,'meteo_socal_mk.amv')

shutil.copyfile(src, dst)

#5
src = os.path.join(meteo_dir,'meteo.amv') 
dst = os.path.join(meteo_dir,'meteo_king_hi.amv')

shutil.copyfile(src, dst)

#6
src = os.path.join(meteo_dir,'meteo.amv') 
dst = os.path.join(meteo_dir,'meteo_king_outer.amv')

shutil.copyfile(src, dst)
