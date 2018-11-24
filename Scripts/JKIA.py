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
from os.path import join as JoinPath

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

		WalkingDistances = self.ReadWalkingDistancesMatrix(JoinPath("Inputs","WalkingDistances.xlsx"))

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
		
		Gates.append(Gate(Name="D2A", DomesticOrInternational="Domestic"))
		Gates.append(Gate(Name="D2B", DomesticOrInternational="Domestic"))
		Gates.append(Gate(Name="D2C", DomesticOrInternational="Domestic"))
		Gates.append(Gate(Name="D3A", DomesticOrInternational="Domestic"))
		Gates.append(Gate(Name="D3B", DomesticOrInternational="Domestic"))
		Gates.append(Gate(Name="D3C", DomesticOrInternational="Domestic"))

		Gates.append(Gate(Name="C4L", DomesticOrInternational="Internal"))
		Gates.append(Gate(Name="C4R", DomesticOrInternational="Internal"))
		Gates.append(Gate(Name="C5" , DomesticOrInternational="Internal"))
		Gates.append(Gate(Name="C6" , DomesticOrInternational="Internal"))

		Gates.append(Gate(Name="B7" , DomesticOrInternational="Internal"))
		Gates.append(Gate(Name="B8" , DomesticOrInternational="Internal"))
		Gates.append(Gate(Name="B9" , DomesticOrInternational="Internal"))
		Gates.append(Gate(Name="B10", DomesticOrInternational="Internal"))
		Gates.append(Gate(Name="B11", DomesticOrInternational="Internal"))

		Gates.append(Gate(Name="A12", DomesticOrInternational="Internal"))
		Gates.append(Gate(Name="A13", DomesticOrInternational="Internal"))
		Gates.append(Gate(Name="A14", DomesticOrInternational="Internal"))
		Gates.append(Gate(Name="A15", DomesticOrInternational="Internal"))
		Gates.append(Gate(Name="A16", DomesticOrInternational="Internal"))
		Gates.append(Gate(Name="A17", DomesticOrInternational="Internal"))
		Gates.append(Gate(Name="A18", DomesticOrInternational="Internal"))
		Gates.append(Gate(Name="A19", DomesticOrInternational="Internal"))
		Gates.append(Gate(Name="A20", DomesticOrInternational="Internal"))


		# for i in range(30):
		# 	Gates.append(Gate(Name="X"+str(i+1)))
		print Gates
		return Gates

	def SetupBays(self):

		Bays = []

		Bays.append(Bay(Name="D2A",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B"])))
		Bays.append(Bay(Name="D2B",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C"])))
		Bays.append(Bay(Name="D2C",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="D3A",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B"])))
		Bays.append(Bay(Name="D3B",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C"])))
		Bays.append(Bay(Name="D3C",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		
		Bays.append(Bay(Name="C4L",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G"])))
		Bays.append(Bay(Name="C4R",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))
		Bays.append(Bay(Name="C5" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
		Bays.append(Bay(Name="C6" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
		
		Bays.append(Bay(Name="B7" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
		Bays.append(Bay(Name="B8" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
		Bays.append(Bay(Name="B9" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
		Bays.append(Bay(Name="B10",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
		Bays.append(Bay(Name="B11",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
		
		Bays.append(Bay(Name="A12",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))
		Bays.append(Bay(Name="A13",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))
		Bays.append(Bay(Name="A14",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))
		Bays.append(Bay(Name="A15",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))
		Bays.append(Bay(Name="A16",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))
		Bays.append(Bay(Name="A17",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G"])))
		Bays.append(Bay(Name="A18",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
		Bays.append(Bay(Name="A19",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
		Bays.append(Bay(Name="A20",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))
		
		Bays.append(Bay(Name="J1" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E","F","G","H"])))
		Bays.append(Bay(Name="J2A",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="J2B",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="J3A",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="J3B",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="J4A",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="J4B",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="J5" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E","F","G","H"])))
		
		Bays.append(Bay(Name="J6" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="J7" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"]),FuelingPossible=False))
		Bays.append(Bay(Name="J8" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"]),FuelingPossible=False))
		Bays.append(Bay(Name="J9" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"]),FuelingPossible=False))

		Bays.append(Bay(Name="H1" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="H2" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="H3" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="H4" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="H5" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="H6" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="H7" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="H8" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="H9" ,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
		Bays.append(Bay(Name="H10",CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))

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