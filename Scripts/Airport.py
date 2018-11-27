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

from datetime import datetime
from openpyxl import load_workbook
from Airlines import AllAirlines

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Internal
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from AirportElements import Bay,Gate

#****************************************************************************************************
# Airport
#****************************************************************************************************

class Airport(object):
    """docstring for Airport"""

    #================================================================================
    # Initialization
    #================================================================================
    
    def __init__(self,Name="TestAirport",T_Open="08:00",T_Close="22:00",Terminals=None, Gates=None,Bays=None,TravelDistances_Gates={},TravelDistances_Bays={},Airlines=None,AddVirtualElements=True):
        super(Airport, self).__init__()

        self.Name = Name

        #--- Schedule ---
        self.T_Open  = T_Open
        self.T_Close = T_Close
        if type(self.T_Open )==str: self.T_Open  = datetime.strptime(self.T_Open,  '%H:%M')
        if type(self.T_Close)==str: self.T_Close = datetime.strptime(self.T_Close, '%H:%M')

        #--- Layout ---
        if not hasattr(self,"Terminals") or Terminals is not None: self.Terminals = Terminals
        if not hasattr(self,"Gates"    ) or Gates     is not None: self.Gates     = Gates
        if not hasattr(self,"Bays"     ) or Bays      is not None: self.Bays      = Bays
        if AddVirtualElements:
            self.CreateVirtualElements()
        self.SetupLayoutDicts()

        #--- TravelDistances ---
        self.TravelDistances_Gates = TravelDistances_Gates
        self.TravelDistances_Bays  = TravelDistances_Bays

        #--- Airlines ---
        if not hasattr(self,"Airlines") or Airlines is not None: self.Airlines = Airlines
        if self.Airlines is None:
            self.Airlines = AllAirlines

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
            if TravelDistanceRow[0] not in ["Terminal","Bay","Gate"]:
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
    # Layout Dicts
    #================================================================================
    
    def SetupLayoutDicts(self,Force=False):

        self.SetupTerminalsDict(Force)
        self.SetupGatesDict(    Force)
        self.SetupBaysDict(     Force)

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Terminals
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
    def SetupTerminalsDict(self,Force=False):
        if hasattr(self,"Terminals_dict") and not Force: return
        self.Terminals_dict = OrderedDict()
        for terminal in self.Terminals:
            self.Terminals_dict[terminal.Name] = terminal

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Gates
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
    def SetupGatesDict(self,Force=False):
        if hasattr(self,"Gates_dict") and not Force: return
        self.Gates_dict = OrderedDict()
        for gate in self.Gates:
            self.Gates_dict[gate.Name] = gate

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Bays
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
    def SetupBaysDict(self,Force=False):
        if hasattr(self,"Bays_dict") and not Force: return
        self.Bays_dict = OrderedDict()
        for bay in self.Bays:
            self.Bays_dict[bay.Name] = bay

    #================================================================================
    # Virtual Elements
    #================================================================================
    
    def CreateVirtualElements(self,per=0.25):

        self.VirtualColor = [0.35]*3
        
        self.CreateVirtualGates(per)
        self.CreateVirtualBays(per)

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Gates
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def CreateVirtualGates(self,per=0.2):
        #----------------------------------------
        # Add Virtual/Infeasible Gates
        #----------------------------------------

        self.VirtualGates = []
        NrVirtualGates = int(len(self.Gates)*per)
        for i in range(NrVirtualGates):
            b = Gate(Name="X"+str(i+1),Color=self.VirtualColor)
            b.Virtual = True
            self.VirtualGates.append(b)
        self.Gates+=self.VirtualGates
        print str(NrVirtualGates)+" VirtualGates have been Created!"

        #----------------------------------------
        # Update TravelDistances
        #----------------------------------------
       
        if 0: # 1:
            for gate in self.VirtualGates:
                for terminal in self.Terminals:
                    self.TravelDistances[(terminal,Gate.Name)] = 24*3600

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Bays
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def CreateVirtualBays(self,per=0.2):
        #----------------------------------------
        # Add Virtual/Infeasible Bays
        #----------------------------------------

        self.VirtualBays = []
        NrVirtualBays = int(len(self.Bays)*per)
        for i in range(NrVirtualBays):
            b = Bay(Name="X"+str(i+1),Color=self.VirtualColor)
            b.Virtual = True
            self.VirtualBays.append(b)
        self.Bays+=self.VirtualBays
        print str(NrVirtualBays)+" VirtualBays have been Created!"

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

    def GetInfoText(self,ShowTravelDistances=False):

        InfoText = ""
        InfoText+="Airport: "+self.Name+"\n"
        InfoText+=" "*3+"T_Open:  "+str(self.T_Open.time()) +"\n"
        InfoText+=" "*3+"T_Close: "+str(self.T_Close.time())+"\n"

        InfoText+=" "*3+"Terminals: ("+str(len(self.Terminals))+") "+str(self.Terminals)+"\n"
        InfoText+=" "*3+"Gates:     ("+str(len(self.Gates    ))+") "+str(self.Gates    )+"\n"
        InfoText+=" "*3+"Bays:      ("+str(len(self.Bays     ))+") "+str(self.Bays     )+"\n"
        if ShowTravelDistances:
            InfoText+=" "*3+"TravelDistances_Gates:  "+str(self.TravelDistances_Gates) +"\n"
            InfoText+=" "*3+"TravelDistances_Bays:   "+str(self.TravelDistances_Bays ) +"\n"
        return InfoText 

    def __repr__(self):
        return self.GetInfoText()

#****************************************************************************************************
# Test Code
#****************************************************************************************************

if __name__=="__main__":
    TestAirport = Airport()
    print TestAirport
