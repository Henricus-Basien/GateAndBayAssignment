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

from datetime import datetime
from openpyxl import load_workbook

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Internal
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#****************************************************************************************************
# Airport
#****************************************************************************************************

class Airport(object):
	"""docstring for Airport"""

	#================================================================================
	# Initialization
	#================================================================================
	
	def __init__(self,Name="TestAirport",T_Open="08:00",T_Close="22:00", Gates=[],Bays=[],WalkingDistances=[]):
		super(Airport, self).__init__()
		self.Name = Name
		self.T_Open  = T_Open
		self.T_Close = T_Close
		if type(self.T_Open)==str:  self.T_Open  = datetime.strptime(self.T_Open,  '%H:%M')
		if type(self.T_Close)==str: self.T_Close = datetime.strptime(self.T_Close, '%H:%M')

		self.Gates = Gates
		self.Bays  = Bays
		self.WalkingDistances = WalkingDistances

	#================================================================================
	# Evaluation
	#================================================================================
	
	def GetOperationalTime(self):
		return (self.T_Close-self.T_Open).total_seconds()

	def ReadWalkingDistancesMatrix(self,filepath):

		wb = load_workbook(filepath)
		print wb
		WalkingDistances = dict()

		WalkingDistancesloadedExcel = load_workbook(filepath)
		WalkingDistancesWorksheet = WalkingDistancesloadedExcel.active
		for WalkingDistanceRow in WalkingDistancesWorksheet.values:
			if WalkingDistanceRow[0] in ["Terminal"]:
				Terminals = []
				for terminals_readout in range(len(WalkingDistanceRow)-1):
					terminals_readout += 1
					Terminals.append(str(WalkingDistanceRow[terminals_readout]))
			if WalkingDistanceRow[0] not in ["Terminal","Bay"]:
				if WalkingDistanceRow[0] != None:
					WalkingDistanceGate = str(WalkingDistanceRow[0])
					t_counter = 0
					for Distance in WalkingDistanceRow:
						if Distance == WalkingDistanceGate:
							print Distance
						else:
							WalkingDistances[(Terminals[t_counter],WalkingDistanceGate)] = int(Distance)
							t_counter += 1

		return WalkingDistances

	#================================================================================
	# Info
	#================================================================================

	def PrintInfo(self):

		print self.GetInfoText()

	def GetInfoText(self):

		InfoText = ""
		InfoText+="Airport: "+self.Name+"\n"
		InfoText+=" "*3+"T_Open:  "+str(self.T_Open.time()) +"\n"
		InfoText+=" "*3+"T_Close: "+str(self.T_Close.time())+"\n"

		InfoText+=" "*3+"Gates: "+str(self.Gates)+"\n"
		InfoText+=" "*3+"Bays:  "+str(self.Bays) +"\n"
		InfoText+=" "*3+"WalkingDistances:  "+str(self.WalkingDistances) +"\n"
		return InfoText	

	def __repr__(self):
		return self.GetInfoText()

#****************************************************************************************************
# Test Code
#****************************************************************************************************

if __name__=="__main__":
	TestAirport = Airport()
	print TestAirport
