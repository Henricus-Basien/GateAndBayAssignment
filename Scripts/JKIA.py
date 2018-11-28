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

from copy import copy
from collections import OrderedDict
from os.path import join as JoinPath

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Internal
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from Airport         import Airport
from AirportElements import Terminal,Gate,Bay
from Airlines        import AllAirlines

#****************************************************************************************************
# JKIA
#****************************************************************************************************

class JKIA(Airport):
    """docstring for JKIA"""

    #================================================================================
    # Initialization
    #================================================================================

    def __init__(self):

        T_Open  = "06:00"
        T_Close = "23:59"#"09:00"#"18:00"#"23:59"#"12:00"# "23:59"#"12:00"#"18:00"#"23:59"#"18:00"#"12:00"#"23:59"

        TravelDistances_Bays  = self.ReadTravelDistancesMatrix(JoinPath("Inputs","JKIA-TravelDistances_Bays.xlsx"))
        TravelDistances_Gates = self.ReadTravelDistancesMatrix(JoinPath("Inputs","JKIA-TravelDistances_Bays.xlsx")) # ToDo Needs to be fixed!

        #--- Airline/Aircraft ---
        self.SetupAirlines()
        self.LocalAirline = "KQ"
        self.SetupAircraftGroups()

        #--- Layout ---
        self.SetupTerminals()
        self.SetupGates()
        self.SetupBays()

        #--- Setup Airport ---
        super(JKIA, self).__init__(Name="JKIA",T_Open=T_Open,T_Close=T_Close,TravelDistances_Bays=TravelDistances_Bays,TravelDistances_Gates=TravelDistances_Gates)

    #================================================================================
    # Airlines/Aircraft
    #================================================================================

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Airlines
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def SetupAirlines(self):

        self.Airlines = []

        for airline in AllAirlines:
            airline = copy(airline)

            if   airline.Name=="KQ" : airline.Terminal = "D"
            elif airline.Name=="KLM": airline.Terminal = "A"
            elif airline.Name=="EK" : airline.Terminal = "A"
            elif airline.Name=="ET" : airline.Terminal = "A"
            elif airline.Name=="EY" : airline.Terminal = "A"
            elif airline.Name=="G"  : airline.Terminal = "A"
            elif airline.Name=="LX" : airline.Terminal = "A"
            elif airline.Name=="MK" : airline.Terminal = "A"
            elif airline.Name=="MS" : airline.Terminal = "A"
            elif airline.Name=="PW" : airline.Terminal = "A"
            elif airline.Name=="QR" : airline.Terminal = "A"
            elif airline.Name=="SA" : airline.Terminal = "A"
            elif airline.Name=="SN" : airline.Terminal = "A"
            elif airline.Name=="TK" : airline.Terminal = "A"
            elif airline.Name=="TM" : airline.Terminal = "A"
            elif airline.Name=="CZ" : airline.Terminal = "A"
            elif airline.Name=="WB" : airline.Terminal = "A"
            elif airline.Name=="BA" : airline.Terminal = "A"
            elif airline.Name=="SV" : airline.Terminal = "A"
            else:
                print "WARNING: Airline '"+airline.Name+"' has no preferably assigned Terminal!!!"
                airline.Terminal = "A"

            self.Airlines.append(airline)

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Aircraft Groups
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
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

    #================================================================================
    # Layout
    #================================================================================

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Terminals
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    def SetupTerminals(self):

        self.Terminals = []

        self.Terminals.append(Terminal(Name="A",Color=[0.0,0.0,1.0]))
        self.Terminals.append(Terminal(Name="B",Color=[1.0,0.8,0.0]))
        self.Terminals.append(Terminal(Name="C",Color=[0.8,1.0,0.0]))
        self.Terminals.append(Terminal(Name="D",Color=[0.0,1.0,0.0]))

        self.SetupTerminalsDict()

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Gates
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def SetupGates(self):

        self.Gates = []
        
        self.Gates.append(Gate(Name="A12",Color=self.Terminals_dict["A"].Color, DestinationType="International"))
        self.Gates.append(Gate(Name="A13",Color=self.Terminals_dict["A"].Color, DestinationType="International"))
        self.Gates.append(Gate(Name="A14",Color=self.Terminals_dict["A"].Color, DestinationType="International"))
        # self.Gates.append(Gate(Name="A15",Color=self.Terminals_dict["A"].Color, DestinationType="International"))
        self.Gates.append(Gate(Name="A16",Color=self.Terminals_dict["A"].Color, DestinationType="International"))
        self.Gates.append(Gate(Name="A17",Color=self.Terminals_dict["A"].Color, DestinationType="International"))
        self.Gates.append(Gate(Name="A18",Color=self.Terminals_dict["A"].Color, DestinationType="International"))
        self.Gates.append(Gate(Name="A19",Color=self.Terminals_dict["A"].Color, DestinationType="International"))
        self.Gates.append(Gate(Name="A20",Color=self.Terminals_dict["A"].Color, DestinationType="International"))

        self.Gates.append(Gate(Name="B7" ,Color=self.Terminals_dict["B"].Color, DestinationType="Mixed"))
        self.Gates.append(Gate(Name="B8" ,Color=self.Terminals_dict["B"].Color, DestinationType="Mixed"))
        self.Gates.append(Gate(Name="B9" ,Color=self.Terminals_dict["B"].Color, DestinationType="Mixed"))
        self.Gates.append(Gate(Name="B10",Color=self.Terminals_dict["B"].Color, DestinationType="Mixed"))
        self.Gates.append(Gate(Name="B11",Color=self.Terminals_dict["B"].Color, DestinationType="Mixed"))

        self.Gates.append(Gate(Name="C4L",Color=self.Terminals_dict["C"].Color, DestinationType="Mixed"))
        self.Gates.append(Gate(Name="C4R",Color=self.Terminals_dict["C"].Color, DestinationType="Mixed"))
        self.Gates.append(Gate(Name="C5" ,Color=self.Terminals_dict["C"].Color, DestinationType="Mixed"))
        self.Gates.append(Gate(Name="C6" ,Color=self.Terminals_dict["C"].Color, DestinationType="Mixed"))

        self.Gates.append(Gate(Name="D2A",Color=self.Terminals_dict["D"].Color, DestinationType="Domestic"))
        self.Gates.append(Gate(Name="D2B",Color=self.Terminals_dict["D"].Color, DestinationType="Domestic"))
        self.Gates.append(Gate(Name="D2C",Color=self.Terminals_dict["D"].Color, DestinationType="Domestic"))
        self.Gates.append(Gate(Name="D3A",Color=self.Terminals_dict["D"].Color, DestinationType="Domestic"))
        self.Gates.append(Gate(Name="D3B",Color=self.Terminals_dict["D"].Color, DestinationType="Domestic"))
        self.Gates.append(Gate(Name="D3C",Color=self.Terminals_dict["D"].Color, DestinationType="Domestic"))       

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Bays
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def SetupBays(self):

        self.Bays = []

        #----------------------------------------
        # Terminal Bays
        #----------------------------------------

        self.Bays.append(Bay(Name="A12",Color=self.Terminals_dict["A"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))
        self.Bays.append(Bay(Name="A13",Color=self.Terminals_dict["A"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))
        self.Bays.append(Bay(Name="A14",Color=self.Terminals_dict["A"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))
        self.Bays.append(Bay(Name="A16",Color=self.Terminals_dict["A"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))
        self.Bays.append(Bay(Name="A17",Color=self.Terminals_dict["A"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G"])))
        self.Bays.append(Bay(Name="A18",Color=self.Terminals_dict["A"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
        self.Bays.append(Bay(Name="A19",Color=self.Terminals_dict["A"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
        self.Bays.append(Bay(Name="A20",Color=self.Terminals_dict["A"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))

        self.Bays.append(Bay(Name="B7" ,Color=self.Terminals_dict["B"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
        self.Bays.append(Bay(Name="B8" ,Color=self.Terminals_dict["B"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
        self.Bays.append(Bay(Name="B9" ,Color=self.Terminals_dict["B"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
        self.Bays.append(Bay(Name="B10",Color=self.Terminals_dict["B"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
        self.Bays.append(Bay(Name="B11",Color=self.Terminals_dict["B"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))

        self.Bays.append(Bay(Name="C4L",Color=self.Terminals_dict["C"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G"])))
        self.Bays.append(Bay(Name="C4R",Color=self.Terminals_dict["C"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))
        self.Bays.append(Bay(Name="C5" ,Color=self.Terminals_dict["C"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
        self.Bays.append(Bay(Name="C6" ,Color=self.Terminals_dict["C"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))

        self.Bays.append(Bay(Name="D2A",Color=self.Terminals_dict["D"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B"])))
        self.Bays.append(Bay(Name="D2B",Color=self.Terminals_dict["D"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C"])))
        self.Bays.append(Bay(Name="D2C",Color=self.Terminals_dict["D"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        self.Bays.append(Bay(Name="D3A",Color=self.Terminals_dict["D"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B"])))
        self.Bays.append(Bay(Name="D3B",Color=self.Terminals_dict["D"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C"])))
        self.Bays.append(Bay(Name="D3C",Color=self.Terminals_dict["D"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        
        #----------------------------------------
        # External Bays
        #----------------------------------------
        
        J_Color = [0.8]*3
        H_Color = [0.6]*3

        self.Bays.append(Bay(Name="J1" ,Color=J_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E","F","G","H"])))
        self.Bays.append(Bay(Name="J2A",Color=J_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        self.Bays.append(Bay(Name="J2B",Color=J_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        self.Bays.append(Bay(Name="J3A",Color=J_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        self.Bays.append(Bay(Name="J3B",Color=J_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        self.Bays.append(Bay(Name="J4A",Color=J_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        self.Bays.append(Bay(Name="J4B",Color=J_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        self.Bays.append(Bay(Name="J5" ,Color=J_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E","F","G","H"])))
        
        self.Bays.append(Bay(Name="J6" ,Color=J_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        self.Bays.append(Bay(Name="J7" ,Color=J_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"]),FuelingPossible=False))
        self.Bays.append(Bay(Name="J8" ,Color=J_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"]),FuelingPossible=False))
        self.Bays.append(Bay(Name="J9" ,Color=J_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"]),FuelingPossible=False))

        self.Bays.append(Bay(Name="H1" ,Color=H_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        self.Bays.append(Bay(Name="H2" ,Color=H_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        self.Bays.append(Bay(Name="H3" ,Color=H_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        self.Bays.append(Bay(Name="H4" ,Color=H_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        self.Bays.append(Bay(Name="H5" ,Color=H_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        self.Bays.append(Bay(Name="H6" ,Color=H_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        self.Bays.append(Bay(Name="H7" ,Color=H_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        self.Bays.append(Bay(Name="H8" ,Color=H_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        self.Bays.append(Bay(Name="H9" ,Color=H_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        self.Bays.append(Bay(Name="H10",Color=H_Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))

#****************************************************************************************************
# Test Code
#****************************************************************************************************

if __name__=="__main__":
    JKIA = JKIA()
    print JKIA
