# -*- coding: utf-8 -*-
'''
Created on Wednesday 21.11.2018
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

# from collections import OrderedDict

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Internal
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from AircraftTypes import All_AircraftTypes,GetAircraftsByType

#****************************************************************************************************
# Airlines
#****************************************************************************************************

class Airline(object):
	"""docstring for Airline"""

	#================================================================================
	# Initialization
	#================================================================================
	
	def __init__(self,Name="TestAirline", AircraftTypes=All_AircraftTypes):
		super(Airline, self).__init__()
		self.Name = Name
		self.AircraftTypes = AircraftTypes

	#================================================================================
	# Info
	#================================================================================
	
	def GetInfoText(self):

		InfoText = ""

		InfoText+="Airline - "+self.Name+": "+"\n"
		for aircraft_t in self.AircraftTypes:
			InfoText+=" "*3+str(aircraft_t)

		return InfoText

	def __repr__(self):

		return self.GetInfoText()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# All Airlines
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

AllAirlines = []
AllAirlines.append(Airline("KQ" , AircraftTypes=GetAircraftsByType(["B737", "B738", "B73J", "B773", "B778", "B788", "E90", "AT7"])))
AllAirlines.append(Airline("KLM", AircraftTypes=GetAircraftsByType(["B747"                                                      ])))
AllAirlines.append(Airline("EK" , AircraftTypes=GetAircraftsByType(["B773"                                                      ])))
AllAirlines.append(Airline("ET" , AircraftTypes=GetAircraftsByType(["B737", "B738"                                              ])))
AllAirlines.append(Airline("EY" , AircraftTypes=GetAircraftsByType(["A320"                                                      ])))
AllAirlines.append(Airline("G"  , AircraftTypes=GetAircraftsByType(["A320"                                                      ])))
AllAirlines.append(Airline("LX" , AircraftTypes=GetAircraftsByType(["A330"                                                      ])))
AllAirlines.append(Airline("MK" , AircraftTypes=GetAircraftsByType(["A332"                                                      ])))
AllAirlines.append(Airline("MS" , AircraftTypes=GetAircraftsByType(["A320"                                                      ])))
AllAirlines.append(Airline("PW" , AircraftTypes=GetAircraftsByType(["AT7"                                                       ])))
AllAirlines.append(Airline("QR" , AircraftTypes=GetAircraftsByType(["A320"                                                      ])))
AllAirlines.append(Airline("SA" , AircraftTypes=GetAircraftsByType(["A320"                                                      ])))
AllAirlines.append(Airline("SN" , AircraftTypes=GetAircraftsByType(["A320", "A332"                                              ])))
AllAirlines.append(Airline("TK" , AircraftTypes=GetAircraftsByType(["A330"                                                      ])))
AllAirlines.append(Airline("TM" , AircraftTypes=GetAircraftsByType(["E90"                                                       ])))
AllAirlines.append(Airline("CZ" , AircraftTypes=GetAircraftsByType(["A330"                                                      ])))
AllAirlines.append(Airline("WB" , AircraftTypes=GetAircraftsByType(["B737", "Q400"                                              ])))
AllAirlines.append(Airline("BA" , AircraftTypes=GetAircraftsByType(["B772"                                                      ])))
AllAirlines.append(Airline("SV" , AircraftTypes=GetAircraftsByType(["A320"                                                      ])))

# #--- Dict ---
# AllAirlines_dict = OrderedDict()
# for airline in AllAirlines:
# 	AllAirlines_dict[airline.Name] = Airline

#****************************************************************************************************
# Test Code
#****************************************************************************************************

if __name__=="__main__":
	for airline in AllAirlines:
		print airline