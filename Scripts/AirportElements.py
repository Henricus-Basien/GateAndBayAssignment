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

#****************************************************************************************************
# AirportElements
#****************************************************************************************************

class AirportElement(object):
	"""docstring for AirportElement"""
	def __init__(self,Name="TestElements"):
		super(AirportElement, self).__init__()
		self.Name = Name
		
	def __repr__(self):
		return self.Name

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Gate
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Gate(AirportElement):
	"""docstring for Gate"""
	def __init__(self, Name="TestGate",DestinationType=None):
		super(Gate, self).__init__(Name)

		DestinationType = DestinationType
		
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Bay
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Bay(AirportElement):
	"""docstring for Bay"""
	def __init__(self, Name="TestBay",CompatibleAircraftTypes=None,FuelingPossible=True):
		super(Bay, self).__init__(Name)

		self.CompatibleAircraftTypes = CompatibleAircraftTypes
		self.FuelingPossible         = FuelingPossible

#****************************************************************************************************
# Test Code
#****************************************************************************************************

if __name__=="__main__":
	TestGate = Gate()
	TestBay  = Bay()

	print TestGate
	print TestBay