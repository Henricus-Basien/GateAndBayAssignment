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
    def __init__(self):

        T_Open  = "06:00"
        T_Close = "23:59"
        
        self.SetTerminals()
        self.SetupAircraftGroups()
        Gates = self.SetupGates()
        Bays  = self.SetupBays()

        TravelDistances = self.ReadTravelDistancesMatrix(JoinPath("Inputs","JKIA-TravelDistances.xlsx"))
        if hasattr(self,"VirtualBays"):
            for bay in self.VirtualBays:
                for terminal in self.Terminals:
                    TravelDistances[(terminal,bay.Name)] = 10**9

        super(JKIA, self).__init__(Name="JKIA",T_Open=T_Open,T_Close=T_Close,Gates=Gates,Bays=Bays,TravelDistances=TravelDistances)

        self.SetAirlines()

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Terminals
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    def SetTerminals(self):

        self.Terminals = OrderedDict()

        self.Terminals["A"] = Terminal(Name="A",Color=[0.0,0.0,1.0])
        self.Terminals["B"] = Terminal(Name="B",Color=[1.0,0.8,0.0])
        self.Terminals["C"] = Terminal(Name="C",Color=[0.8,1.0,0.0])
        self.Terminals["D"] = Terminal(Name="D",Color=[0.0,1.0,0.0])

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Airlines
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def SetAirlines(self):

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

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Gates
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def SetupGates(self):

        Gates = []
        
        Gates.append(Gate(Name="A12",Color=self.Terminals["A"].Color, DestinationType="International"))
        Gates.append(Gate(Name="A13",Color=self.Terminals["A"].Color, DestinationType="International"))
        Gates.append(Gate(Name="A14",Color=self.Terminals["A"].Color, DestinationType="International"))
        Gates.append(Gate(Name="A15",Color=self.Terminals["A"].Color, DestinationType="International"))
        Gates.append(Gate(Name="A16",Color=self.Terminals["A"].Color, DestinationType="International"))
        Gates.append(Gate(Name="A17",Color=self.Terminals["A"].Color, DestinationType="International"))
        Gates.append(Gate(Name="A18",Color=self.Terminals["A"].Color, DestinationType="International"))
        Gates.append(Gate(Name="A19",Color=self.Terminals["A"].Color, DestinationType="International"))
        Gates.append(Gate(Name="A20",Color=self.Terminals["A"].Color, DestinationType="International"))

        Gates.append(Gate(Name="B7" ,Color=self.Terminals["B"].Color, DestinationType="Mixed"))
        Gates.append(Gate(Name="B8" ,Color=self.Terminals["B"].Color, DestinationType="Mixed"))
        Gates.append(Gate(Name="B9" ,Color=self.Terminals["B"].Color, DestinationType="Mixed"))
        Gates.append(Gate(Name="B10",Color=self.Terminals["B"].Color, DestinationType="Mixed"))
        Gates.append(Gate(Name="B11",Color=self.Terminals["B"].Color, DestinationType="Mixed"))

        Gates.append(Gate(Name="C4L",Color=self.Terminals["C"].Color, DestinationType="Mixed"))
        Gates.append(Gate(Name="C4R",Color=self.Terminals["C"].Color, DestinationType="Mixed"))
        Gates.append(Gate(Name="C5" ,Color=self.Terminals["C"].Color, DestinationType="Mixed"))
        Gates.append(Gate(Name="C6" ,Color=self.Terminals["C"].Color, DestinationType="Mixed"))

        Gates.append(Gate(Name="D2A",Color=self.Terminals["D"].Color, DestinationType="Domestic"))
        Gates.append(Gate(Name="D2B",Color=self.Terminals["D"].Color, DestinationType="Domestic"))
        Gates.append(Gate(Name="D2C",Color=self.Terminals["D"].Color, DestinationType="Domestic"))
        Gates.append(Gate(Name="D3A",Color=self.Terminals["D"].Color, DestinationType="Domestic"))
        Gates.append(Gate(Name="D3B",Color=self.Terminals["D"].Color, DestinationType="Domestic"))
        Gates.append(Gate(Name="D3C",Color=self.Terminals["D"].Color, DestinationType="Domestic"))       

        return Gates

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Bays
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def SetupBays(self):

        Bays = []

        #----------------------------------------
        # Terminal Bays
        #----------------------------------------

        Bays.append(Bay(Name="A12",Color=self.Terminals["A"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))
        Bays.append(Bay(Name="A13",Color=self.Terminals["A"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))
        Bays.append(Bay(Name="A14",Color=self.Terminals["A"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))
        Bays.append(Bay(Name="A16",Color=self.Terminals["A"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))
        Bays.append(Bay(Name="A17",Color=self.Terminals["A"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G"])))
        Bays.append(Bay(Name="A18",Color=self.Terminals["A"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
        Bays.append(Bay(Name="A19",Color=self.Terminals["A"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
        Bays.append(Bay(Name="A20",Color=self.Terminals["A"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))

        Bays.append(Bay(Name="B7" ,Color=self.Terminals["B"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
        Bays.append(Bay(Name="B8" ,Color=self.Terminals["B"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
        Bays.append(Bay(Name="B9" ,Color=self.Terminals["B"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
        Bays.append(Bay(Name="B10",Color=self.Terminals["B"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
        Bays.append(Bay(Name="B11",Color=self.Terminals["B"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))

        Bays.append(Bay(Name="C4L",Color=self.Terminals["C"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G"])))
        Bays.append(Bay(Name="C4R",Color=self.Terminals["C"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E"])))
        Bays.append(Bay(Name="C5" ,Color=self.Terminals["C"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))
        Bays.append(Bay(Name="C6" ,Color=self.Terminals["C"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["B","C","D","E","F","G","H"])))

        Bays.append(Bay(Name="D2A",Color=self.Terminals["D"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B"])))
        Bays.append(Bay(Name="D2B",Color=self.Terminals["D"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C"])))
        Bays.append(Bay(Name="D2C",Color=self.Terminals["D"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        Bays.append(Bay(Name="D3A",Color=self.Terminals["D"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B"])))
        Bays.append(Bay(Name="D3B",Color=self.Terminals["D"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C"])))
        Bays.append(Bay(Name="D3C",Color=self.Terminals["D"].Color,CompatibleAircraftTypes=self.GetAircraftTypesByGroup(["A","B","C","D","E"])))
        
        #----------------------------------------
        # External Bays
        #----------------------------------------
        
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

        #----------------------------------------
        # Virtual/Infeasible Bays
        #----------------------------------------
        
        if 1:
            self.VirtualBays = []
            for i in range(int(len(Bays)*0.1)):
                self.VirtualBays.append(Bay(Name="X"+str(i+1),Color=[0]*3))
            Bays+=self.VirtualBays

        return Bays

#****************************************************************************************************
# Test Code
#****************************************************************************************************

if __name__=="__main__":
    JKIA = JKIA()
    print JKIA
