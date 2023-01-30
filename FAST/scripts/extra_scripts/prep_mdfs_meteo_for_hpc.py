# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 12:20:41 2022

@author: schroderk
"""
#setup setup step
#basic code to name mdf files accoring to their respective domains - which is needed for the CoSMoS model to run on the HPC
from pathlib2 import Path

#location where mdfs are  (change as needed)
mdf_dir = r'C:\Users\klaus\Desktop\SLR200_NA_warmstart'

#1. mdelrey_hi
# Creating a function to
# replace the text
def replacetext(search_text, replace_text):
  
    # Opening the file using the Path function
    file = Path(mdf_dir, "mdelrey_hi.mdf")
  
    # Reading and storing the content of the file in
    # a data variable
    data = file.read_text()
  
    # Replacing the text using the replace function
    data = data.replace(search_text, replace_text)
  
    # Writing the replaced data
    # in the text file
    file.write_text(data)
  
    # Return "Text replaced" string
    return "Text replaced"
  
  
# Creating a variable and storing
# the text that we want to search
search_text = "meteo"
  
# Creating a variable and storing
# the text that we want to update
replace_text = "meteo_mdelrey_hi"
  
# Calling the replacetext function
replacetext(search_text, replace_text)

#2. mdelrey_outer
def replacetext(search_text, replace_text):
    file = Path(mdf_dir, "mdelrey_outer.mdf")
    data = file.read_text()
    data = data.replace(search_text, replace_text)
    file.write_text(data)
    return "Text replaced"

search_text = "meteo"
replace_text = "meteo_mdelrey_outer"
replacetext(search_text, replace_text)

#3. canals
def replacetext(search_text, replace_text):
    file = Path(mdf_dir, "canals.mdf")
    data = file.read_text()
    data = data.replace(search_text, replace_text)
    file.write_text(data)
    return "Text replaced"

search_text = "meteo"
replace_text = "meteo_canals"
replacetext(search_text, replace_text)

#4. king_hi
def replacetext(search_text, replace_text):
    file = Path(mdf_dir, "king_hi.mdf")
    data = file.read_text()
    data = data.replace(search_text, replace_text)
    file.write_text(data)
    return "Text replaced"

search_text = "meteo"
replace_text = "meteo_king_hi"
replacetext(search_text, replace_text)

#5. king_outer
def replacetext(search_text, replace_text):
    file = Path(mdf_dir, "king_outer.mdf")
    data = file.read_text()
    data = data.replace(search_text, replace_text)
    file.write_text(data)
    return "Text replaced"

search_text = "meteo"
replace_text = "meteo_king_outer"
replacetext(search_text, replace_text)

#6. socal_mk
def replacetext(search_text, replace_text):
    file = Path(mdf_dir, "socal_mk.mdf")
    data = file.read_text()
    data = data.replace(search_text, replace_text)
    file.write_text(data)
    return "Text replaced"

search_text = "meteo"
replace_text = "meteo_socal_mk"
replacetext(search_text, replace_text)



