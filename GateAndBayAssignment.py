# -*- coding: utf-8 -*-
'''
Created on Tuesday 20.11.2018
Copyright (©) Henricus N. Basien
Author: Henricus N. Basien, Pavel Volkov
Email: Henricus@Basien.de
'''

#****************************************************************************************************
# Imports
#****************************************************************************************************

import os,sys
RootPath = os.path.split(__file__)[0]
sys.path.insert(0,os.path.join(RootPath,"Scripts"))

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# External
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Internal
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from ScheduleCreator import ScheduleCreator

#****************************************************************************************************
# GateAndBayAssignment
#****************************************************************************************************

class GateAndBayAssignmentSolver(object):
	"""docstring for GateAndBayAssignmentSolver"""

	#================================================================================
	# Initialization
	#================================================================================
	
	def __init__(self, Airport,Schedule=None,LP_Path="Temp",AutoRun=True):
		super(GateAndBayAssignmentSolver, self).__init__()
		#--- Set Settings ---
		self.Airport  = Airport
		self.Schedule = Schedule

		self.LP_Path = os.path.realpath(LP_Path)

		#--- Schedule ---
		if self.Schedule is None:
			MaxNrAircraft  = len(self.Airport.Bays)
			self.Scheduler = ScheduleCreator(self.Airport,MaxNrOverlappingAircraft=MaxNrAircraft,ScheduleFolder="Schedules",AutoRun=False)
			self.Scheduler.Run(Visualize=True)
			self.Schedule  = self.Scheduler.Schedule

		#--- Run ---
		if AutoRun:
			self.Run()

	#================================================================================
	# Run Assignment
	#================================================================================
	
	def Run(self):

		self.CreateLP()

	def CreateLP(self):

		LP = []

		LP+=self.GetLP_ExclusionConstraints()

		if not os.path.exists(self.LP_Path): os.makedirs(self.LP_Path)
		with open(os.path.join(self.LP_Path,"LP.txt"),"w") as LP_File:
			for line in LP:
				LP_File.write(line+"\n")

	def GetLP_ExclusionConstraints(self):

		ExclusionConstraints = []

		for aircraft1 in self.Schedule:
			for aircraft2 in self.Schedule:
				ExclusionConstraints.append("X_"+aircraft1.ID+"!="+"X_"+aircraft2.ID)

		return ExclusionConstraints
		
#****************************************************************************************************
# Test Code
#****************************************************************************************************

if __name__=="__main__":

	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	# Imports
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	
	from JKIA import JKIA

	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	# Run Test
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	
	airport = JKIA()
	airport.PrintInfo()

	GABA_Solver = GateAndBayAssignmentSolver(airport)