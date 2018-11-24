# -*- coding: utf-8 -*-
'''
Created on Tuesday 20.11.2018
Copyright (©) Henricus N. Basien
Author: Henricus N. Basien
Email: Henricus@Basien.de
'''

#****************************************************************************************************
# Imports
#****************************************************************************************************

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# External
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# from collections import OrderedDict

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Internal
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from Airport import Airport
from AirportElements import Gate,Bay

#****************************************************************************************************
# JKIA
#****************************************************************************************************

class JKIA(Airport):
	"""docstring for JKIA"""
	def __init__(self):

		T_Open  = "06:00"
		T_Close = "23:59"
		Gates = self.SetupGates()
		Bays  = self.SetupBays()

		WalkingDistances = []

		super(JKIA, self).__init__(Name="JKIA",T_Open=T_Open,T_Close=T_Close,Gates=Gates,Bays=Bays,WalkingDistances=WalkingDistances)

	def SetupGates(self):

		Gates = []
		for i in range(30):
			Gates.append(Gate(Name="X"+str(i+1)))

		return Gates

	def SetupBays(self):

		Bays = []
		for i in range(30):
			Bays.append(Bay(Name="X"+str(i+1)))

		return Bays

#****************************************************************************************************
# Test Code
#****************************************************************************************************

if __name__=="__main__":
	JKIA = JKIA()
	print JKIA