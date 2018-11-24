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
		return InfoText	

	def __repr__(self):
		return self.GetInfoText()

#****************************************************************************************************
# Test Code
#****************************************************************************************************

if __name__=="__main__":
	TestAirport = Airport()
	print TestAirport