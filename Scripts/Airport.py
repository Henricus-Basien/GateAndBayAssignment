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
from openpyxl import load_workbook
from Airlines import AllAirlines

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Internal
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from AirportElements import Bay

#****************************************************************************************************
# Airport
#****************************************************************************************************

class Airport(object):
    """docstring for Airport"""

    #================================================================================
    # Initialization
    #================================================================================
    
    def __init__(self,Name="TestAirport",T_Open="08:00",T_Close="22:00", Gates=[],Bays=[],TravelDistances={},Airlines=None,AddVirtualBays=True):
        super(Airport, self).__init__()
        self.Name = Name
        self.T_Open  = T_Open
        self.T_Close = T_Close
        if type(self.T_Open)==str:  self.T_Open  = datetime.strptime(self.T_Open,  '%H:%M')
        if type(self.T_Close)==str: self.T_Close = datetime.strptime(self.T_Close, '%H:%M')

        self.Gates = Gates
        self.Bays  = Bays
        self.TravelDistances = TravelDistances
        if Airlines is None:
            Airlines = AllAirlines
        self.Airlines = Airlines

        if AddVirtualBays:
            self.CreateVirtualBays()

    #================================================================================
    # Evaluation
    #================================================================================
    
    def GetOperationalTime(self):
        return (self.T_Close-self.T_Open).total_seconds()

    def ReadTravelDistancesMatrix(self,filepath):

        TravelDistances = dict()

        TravelDistancesloadedExcel = load_workbook(filepath)
        TravelDistancesWorksheet = TravelDistancesloadedExcel.active
        for TravelDistanceRow in TravelDistancesWorksheet.values:
            if TravelDistanceRow[0] in ["Terminal"]:
                Terminals = []
                for terminals_readout in range(len(TravelDistanceRow)-1):
                    terminals_readout += 1
                    Terminals.append(str(TravelDistanceRow[terminals_readout]))
            if TravelDistanceRow[0] not in ["Terminal","Bay"]:
                if TravelDistanceRow[0] != None:
                    TravelDistanceGate = str(TravelDistanceRow[0])
                    t_counter = 0
                    for Distance in TravelDistanceRow:
                        if Distance == TravelDistanceGate:
                            pass #print Distance
                        else:
                            TravelDistances[(Terminals[t_counter],TravelDistanceGate)] = int(Distance)
                            t_counter += 1

        return TravelDistances

    #================================================================================
    # Virtual Bays
    #================================================================================
    
    def CreateVirtualBays(self,per=0.2):
        #----------------------------------------
        # Add Virtual/Infeasible Bays
        #----------------------------------------

        self.VirtualBays = []
        NrVirtualBays = int(len(self.Bays)*per)
        for i in range(NrVirtualBays):
            b = Bay(Name="X"+str(i+1),Color=[0]*3)
            b.Virtual = True
            self.VirtualBays.append(b)
        self.Bays+=self.VirtualBays
        print str(NrVirtualBays)+" have been Created!"

        #----------------------------------------
        # Update TravelDistances
        #----------------------------------------
       
        if 0: # 1:
            for bay in self.VirtualBays:
                for terminal in self.Terminals:
                    self.TravelDistances[(terminal,bay.Name)] = 24*3600

    #================================================================================
    # Info
    #================================================================================

    def PrintInfo(self):

        print self.GetInfoText()

    def GetInfoText(self):

        InfoText = ""
        InfoText+="Airport: "+self.Name+"\n"
        InfoText+=" "*3+"T_Open:  "+str(self.T_Open.time()) +"\n"
        InfoText+=" "*3+"T_Close: "+str(self.T_Close.time())+"\n"

        InfoText+=" "*3+"Gates: ("+str(len(self.Gates))+") "+str(self.Gates)+"\n"
        InfoText+=" "*3+"Bays:  ("+str(len(self.Bays)) +") "+str(self.Bays) +"\n"
        InfoText+=" "*3+"TravelDistances:  "+str(self.TravelDistances) +"\n"
        return InfoText 

    def __repr__(self):
        return self.GetInfoText()

#****************************************************************************************************
# Test Code
#****************************************************************************************************

if __name__=="__main__":
    TestAirport = Airport()
    print TestAirport
