# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 16:03:29 2018

@author: Mussina
"""
import configparser
 
config = configparser.ConfigParser()
config.read('./config/config.ini')

temp = config.get('Stock', 'ToBeAnalysisStock')
ToBeAnalysisStock = temp.split(",")
print("ToBeAnalysisStock:",ToBeAnalysisStock)
