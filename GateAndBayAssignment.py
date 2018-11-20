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

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Internal
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from ScheduleCreator import ScheduleCreator

#****************************************************************************************************
# GateAndBayAssignment
#****************************************************************************************************

class GateAndBayAssignmentSolver(object):
	"""docstring for GateAndBayAssignmentSolver"""
	def __init__(self, Airport,Schedule=None):
		super(GateAndBayAssignmentSolver, self).__init__()
		self.Airport = Airport
		self.Schedule = Schedule
		if self.Schedule is None:
			MaxNrAircraft  = len(self.Airport.Bays)
			self.Scheduler = ScheduleCreator(self.Airport,MaxNrOverlappingAircraft=MaxNrAircraft)
			self.Schedule  = self.Scheduler.Schedule
		
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