# -*- coding: utf-8 -*-
'''
Created on Monday 19.11.2018
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

import os
import openpyxl
from datetime import datetime
# from collections import OrderedDict
import numpy as np

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Internal
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from AircraftTypes import All_AircraftTypes

#****************************************************************************************************
# ScheduleCreator
#****************************************************************************************************

class ScheduleCreator(object):
	"""docstring for ScheduleCreator"""
	def __init__(self, Airport,MaxNrAircraft=None,MaxNrOverlappingAircraft=30,AircraftTypes=All_AircraftTypes,ScheduleFolder="Temp",AutoRun=True):
		super(ScheduleCreator, self).__init__()

		self.Airport                  = Airport
		self.MaxNrAircraft            = MaxNrAircraft
		self.MaxNrOverlappingAircraft = MaxNrOverlappingAircraft
		self.AircraftTypes            = AircraftTypes

		self.ScheduleFolder = os.path.realpath(ScheduleFolder)
		if not os.path.exists(self.ScheduleFolder): os.makedirs(self.ScheduleFolder)

		if self.MaxNrAircraft is None:
			self.MaxNrAircraft = int((self.Airport.GetOperationalTime()/3600.)*self.MaxNrOverlappingAircraft)

		if AutoRun:
			self.CreateAircraftSchedule()
			self.PrintSchedule()
			self.ExportScheduleToExcel()
		
	def CreateAircraftSchedule(self):

		self.Schedule = []

		dt0 = datetime(year=1900,month=1,day=1)

		for i in range(self.MaxNrAircraft):
			AircraftType = np.random.choice(self.AircraftTypes)
			ID = i+1
			Arrival   = np.random.uniform((self.Airport.T_Open-dt0).total_seconds(),(self.Airport.T_Close-dt0).total_seconds())
			Departure = Arrival+np.random.uniform(45*60,20*3600)
			a = AircraftType(ID=ID, Arrival=Arrival,Departure=Departure)

			self.Schedule.append(a)

		self.Schedule.sort(key=lambda x: x.Arrival)#, reverse=True)

	def PrintSchedule(self):

		for aircraft in self.Schedule:
			aircraft.PrintInfo()

	def ExportScheduleToExcel(self):
		wb = openpyxl.Workbook()
		ws = wb.active

		#----------------------------------------
		# Write Header
		#----------------------------------------
		
		ws.cell(row=1, column=1).value = "ID"
		ws.cell(row=1, column=2).value = "Type"
		ws.cell(row=1, column=3).value = "Arrival"
		ws.cell(row=1, column=4).value = "Departure"

		#----------------------------------------
		# Write Data
		#----------------------------------------

		for i in range(self.MaxNrAircraft):
			aircraft = self.Schedule[i]
			ws.cell(row=i+2, column=1).value = aircraft.ID
			ws.cell(row=i+2, column=2).value = aircraft.Type
			ws.cell(row=i+2, column=3).value = aircraft.Arrival
			ws.cell(row=i+2, column=4).value = aircraft.Departure

		wb.save(os.path.join(self.ScheduleFolder,"Airport '"+str(self.Airport.Name)+"' - Schedule.xlsx"))

#****************************************************************************************************
# Test Code
#****************************************************************************************************

if __name__=="__main__":
	 
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	# Imports
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	
	from Airport import Airport

	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	# Run Test
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	
	airport = Airport()
	airport.PrintInfo()

	SC = ScheduleCreator(airport)