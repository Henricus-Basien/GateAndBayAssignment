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
from copy import copy

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Internal
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from ReferenceDate import GetDate

#****************************************************************************************************
# Aircraft
#****************************************************************************************************

class Aircraft(object):
	"""docstring for Aircraft"""

	#================================================================================
	# Initialization
	#================================================================================
	
	Type = "TestAircraft"
	MaxNrPassengers = 100
	WB              = False

	def __init__(self, ID="FN0",Arrival="00:00",Departure="23:59",Type=None,NrPassengers=None,PrefferedGates=None,NeedsFueling=False):
		super(Aircraft, self).__init__()
		self.ID             = str(ID)        # [str]
		if Type is not None:
			self.Type       = Type           # [str]
		self.Arrival        = Arrival        # [datetime]
		self.Departure      = Departure      # [datetime]
		if   type(self.Arrival)   ==str:   self.Arrival   = datetime.strptime(self.Arrival  , '%H:%M')
		elif type(self.Arrival)   ==float: self.Arrival   = datetime(year=1900,month=1,day=1,seconds=self.Arrival)
		if   type(self.Departure) ==str:   self.Departure = datetime.strptime(self.Departure, '%H:%M')
		elif type(self.Departure) ==float: self.Departure = datetime(year=1900,month=1,day=1,seconds=self.Departure)
		self.NrPassengers   = NrPassengers   # [int]
		self.PrefferedGates = PrefferedGates # [list[int]]
		self.NeedsFueling   = NeedsFueling   # [boolean]

		#--- Arrival/Departure Data ---
		self.Arrival_date   = GetDate(self.Arrival)
		self.Arrival_t      = (self.Arrival  -self.Arrival_date).total_seconds()
		self.Departure_date = GetDate(self.Departure)
		self.Departure_t    = (self.Departure-self.Arrival_date).total_seconds()

		self.GroundTime = self.Departure_t-self.Arrival_t

		#--- Defaults ---
		if self.NrPassengers is None:
			self.NrPassengers = copy(self.MaxNrPassengers)
		
	#================================================================================
	# Evaluate
	#================================================================================
	
	def GetGroundTime(self):
		return (self.Departure-self.Arrival).total_seconds()

	#================================================================================
	# Colors
	#================================================================================
	
	def GetColor(self,Mode=None):
		if Mode=="GroundTime":
			return self.GetColor_GroundTime()
		return [0]*3

	def GetColor_GroundTime(self,GT_Max=10.):
		#--- Get GroundTime ---
		GT = self.GetGroundTime()
		GT/=3600
		#--- Get Percentage ---
		per = GT/GT_Max
		if per>1: per=1
		#--- Get Color ---
		color = [per,1-per,0]
		# print self.Arrival,self.Departure,GT,color
		return color

	#================================================================================
	# Info
	#================================================================================
	
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