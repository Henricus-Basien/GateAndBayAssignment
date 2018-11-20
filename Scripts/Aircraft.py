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

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Internal
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#****************************************************************************************************
# Aircraft
#****************************************************************************************************

class Aircraft(object):
	"""docstring for Aircraft"""
	def __init__(self, ID=0,Arrival="00:00",Departure="23:59",Type="TestAircraft",NrPassengers=0,PrefferedGates=None,NeedsFueling=False):
		super(Aircraft, self).__init__()
		self.ID             = ID             # [str]
		self.Type           = Type           # [str]
		self.Arrival        = Arrival        # [datetime]
		self.Departure      = Departure      # [datetime]
		if type(self.Arrival)  ==str: self.Arrival   = datetime.strptime(self.Arrival  , '%H:%M')
		if type(self.Departure)==str: self.Departure = datetime.strptime(self.Departure, '%H:%M')
		self.NrPassengers   = NrPassengers   # [int]
		self.PrefferedGates = PrefferedGates # [list[int]]
		self.NeedsFueling   = NeedsFueling   # [boolean]
		
	def PrintInfo(self):

		print self.GetInfoText()

	def GetInfoText(self):

		InfoText = ""
		InfoText+="Aircraft: "+str(self.ID)+" ["+str(self.Type)+"]"+"\n"
		InfoText+=" "*3+"Arrival:   "+str(self.Arrival)  +"\n"
		InfoText+=" "*3+"Departure: "+str(self.Departure)+"\n"

		return InfoText

	def __repr__(self):
		return self.GetInfoText()

#****************************************************************************************************
# Test Code
#****************************************************************************************************

if __name__=="__main__":
	TestAircraft = Aircraft()
	print TestAircraft