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

from collections import OrderedDict

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
		self.SetupAircraftGroups()
		Gates = self.SetupGates()
		Bays  = self.SetupBays()

		WalkingDistances = []

		super(JKIA, self).__init__(Name="JKIA",T_Open=T_Open,T_Close=T_Close,Gates=Gates,Bays=Bays,WalkingDistances=WalkingDistances)

	def SetupAircraftGroups(self):

		self.AircraftGroups = OrderedDict()
		self.AircraftGroups["A"] = ["AT4","AT7","Q400"]
		self.AircraftGroups["B"] = ["B733","E70"]
		self.AircraftGroups["C"] = ["E90"]
		self.AircraftGroups["D"] = ["B737","B738","A320"]
		self.AircraftGroups["E"] = ["B73J"]
		self.AircraftGroups["F"] = ["B787","B788","A330","A332","B767"]
		self.AircraftGroups["G"] = ["B772","B773"]
		self.AircraftGroups["H"] = ["B747"]

	def GetAircraftTypesByGroup(self,Groups):
		AircraftTypes = []
		for group in Groups:
			AircraftTypes+=self.AircraftGroups[group]
		return AircraftTypes

	def SetupGates(self):

		Gates = []
		
		Gates.append(Gate(Name="D2A"))
		Gates.append(Gate(Name="D2B"))
		Gates.append(Gate(Name="D2C"))
		Gates.append(Gate(Name="D3A"))
		Gates.append(Gate(Name="D3B"))
		Gates.append(Gate(Name="D3C"))

		Gates.append(Gate(Name="C4L"))
		Gates.append(Gate(Name="C4R"))
		Gates.append(Gate(Name="C5" ))
		Gates.append(Gate(Name="C6" ))

		Gates.append(Gate(Name="B7" ))
		Gates.append(Gate(Name="B8" ))
		Gates.append(Gate(Name="B9" ))
		Gates.append(Gate(Name="B10"))
		Gates.append(Gate(Name="B11"))

		Gates.append(Gate(Name="A12"))
		Gates.append(Gate(Name="A13"))
		Gates.append(Gate(Name="A14"))
		Gates.append(Gate(Name="A15"))
		Gates.append(Gate(Name="A16"))
		Gates.append(Gate(Name="A17"))
		Gates.append(Gate(Name="A18"))
		Gates.append(Gate(Name="A19"))
		Gates.append(Gate(Name="A20"))


		# for i in range(30):
		# 	Gates.append(Gate(Name="X"+str(i+1)))
		print Gates
		return Gates

	def SetupBays(self):

		Bays = []

		Bays.append(Bay(Name="D2A",CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B"])))
		Bays.append(Bay(Name="D2B",CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C"])))
		Bays.append(Bay(Name="D2C",CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="D3A",CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B"])))
		Bays.append(Bay(Name="D3B",CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C"])))
		Bays.append(Bay(Name="D3C",CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		
		Bays.append(Bay(Name="C4L",CompatibleAircraft=self.GetAircraftTypesByGroup(["B","C","D","E","F","G"])))
		Bays.append(Bay(Name="C4R",CompatibleAircraft=self.GetAircraftTypesByGroup(["B","C","D","E"])))
		Bays.append(Bay(Name="C5" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
		Bays.append(Bay(Name="C6" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
		
		Bays.append(Bay(Name="B7" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
		Bays.append(Bay(Name="B8" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
		Bays.append(Bay(Name="B9" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
		Bays.append(Bay(Name="B10",CompatibleAircraft=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
		Bays.append(Bay(Name="B11",CompatibleAircraft=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
		
		Bays.append(Bay(Name="A12",CompatibleAircraft=self.GetAircraftTypesByGroup(["B","C","D","E"])))
		Bays.append(Bay(Name="A13",CompatibleAircraft=self.GetAircraftTypesByGroup(["B","C","D","E"])))
		Bays.append(Bay(Name="A14",CompatibleAircraft=self.GetAircraftTypesByGroup(["B","C","D","E"])))
		Bays.append(Bay(Name="A15",CompatibleAircraft=self.GetAircraftTypesByGroup(["B","C","D","E"])))
		Bays.append(Bay(Name="A16",CompatibleAircraft=self.GetAircraftTypesByGroup(["B","C","D","E"])))
		Bays.append(Bay(Name="A17",CompatibleAircraft=self.GetAircraftTypesByGroup(["B","C","D","E","F","G"])))
		Bays.append(Bay(Name="A18",CompatibleAircraft=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
		Bays.append(Bay(Name="A19",CompatibleAircraft=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
		Bays.append(Bay(Name="A20",CompatibleAircraft=self.GetAircraftTypesByGroup(["B","C","D","E"])))
		
		Bays.append(Bay(Name="J1" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E","F","G","H"])))
		Bays.append(Bay(Name="J2A",CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="J2B",CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="J3A",CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="J3B",CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="J4A",CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="J4B",CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="J5" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E","F","G","H"])))
		
		Bays.append(Bay(Name="J6" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="J7" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="J8" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="J9" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))

		Bays.append(Bay(Name="H1" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="H2" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="H3" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="H4" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="H5" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="H6" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="H7" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="H8" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="H9" ,CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="H10",CompatibleAircraft=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))

		# Bays = []
		# for i in range(30):
		# 	Bays.append(Bay(Name="X"+str(i+1)))

		return Bays

#****************************************************************************************************
# Test Code
#****************************************************************************************************

if __name__=="__main__":
	JKIA = JKIA()
	print JKIA