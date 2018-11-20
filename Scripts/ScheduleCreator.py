# -*- coding: utf-8 -*-
'''
Created on Monday 19.11.2018
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

import os
import openpyxl
import datetime
# from collections import OrderedDict
import numpy as np

import matplotlib.pyplot as plt

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Internal
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from AircraftTypes import All_AircraftTypes
from ReferenceDate import ReferenceDate,GetDate

#****************************************************************************************************
# ScheduleCreator
#****************************************************************************************************

class ScheduleCreator(object):
    """docstring for ScheduleCreator"""

    #================================================================================
    # Initialization
    #================================================================================
    
    def __init__(self, Airport,MaxNrAircraft=None,MaxNrOverlappingAircraft=5,AircraftTypes=All_AircraftTypes,ScheduleFolder="Temp",AutoRun=True):
        super(ScheduleCreator, self).__init__()

        self.Airport                  = Airport
        self.MaxNrAircraft            = MaxNrAircraft
        self.MaxNrOverlappingAircraft = MaxNrOverlappingAircraft
        self.AircraftTypes            = AircraftTypes

        self.ScheduleFolder = os.path.realpath(ScheduleFolder)
        if not os.path.exists(self.ScheduleFolder): os.makedirs(self.ScheduleFolder)

        if self.MaxNrAircraft is None:
            self.MaxNrAircraft = int((self.Airport.GetOperationalTime()/3600.)*self.MaxNrOverlappingAircraft)

        if AutoRun:
            self.CreateAircraftSchedule()
            self.PrintSchedule()
            #self.ExportScheduleToExcel()
            self.Visualize()
        
    #================================================================================
    # Schedule Creator
    #================================================================================

    def CreateAircraftSchedule(self,TimeRange=[45*60,20*3600],Sort=True,dt0=ReferenceDate):

        self.Schedule = []

        dt0 = datetime.datetime(year=1900,month=1,day=1)

        for i in range(self.MaxNrAircraft):
            AircraftType = np.random.choice(self.AircraftTypes)
            ID = i+1
            Arrival   = ReferenceDate + datetime.timedelta(seconds=np.random.uniform((self.Airport.T_Open-dt0).total_seconds(),(self.Airport.T_Close-dt0).total_seconds()))
            Departure = Arrival       + datetime.timedelta(seconds=np.random.uniform(*TimeRange))
            a = AircraftType(ID=ID, Arrival=Arrival,Departure=Departure)

            self.Schedule.append(a)

        if Sort:
            self.Schedule.sort(key=lambda x: x.Arrival)#, reverse=True)

    #================================================================================
    # Export
    #================================================================================

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Print
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    def PrintSchedule(self):

        for aircraft in self.Schedule:
            aircraft.PrintInfo()

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Excel
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def ExportScheduleToExcel(self):
        wb = openpyxl.Workbook()
        ws = wb.active

        #----------------------------------------
        # Write Header
        #----------------------------------------
        
        ws.cell(row=1, column=1).value = "ID"
        ws.cell(row=1, column=2).value = "Type"
        ws.cell(row=1, column=3).value = "Arrival"
        ws.cell(row=1, column=4).value = "Departure"

        #----------------------------------------
        # Write Data
        #----------------------------------------

        for i in range(self.MaxNrAircraft):
            aircraft = self.Schedule[i]
            ws.cell(row=i+2, column=1).value = aircraft.ID
            ws.cell(row=i+2, column=2).value = aircraft.Type
            ws.cell(row=i+2, column=3).value = aircraft.Arrival
            ws.cell(row=i+2, column=4).value = aircraft.Departure

        wb.save(os.path.join(self.ScheduleFolder,"Airport '"+str(self.Airport.Name)+"' - Schedule.xlsx"))

    #================================================================================
    # Visualize
    #================================================================================

    def Visualize(self):
    
        self.ShowGanttChart(Show=False)
        self.ShowAircraftOnGround(Show=False)

        plt.show()

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # GanttChart
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def ShowGanttChart(self,Show=True):

        fig,ax=plt.subplots(figsize=(16,9),dpi=120)

        #----------------------------------------
        # Preprocess
        #----------------------------------------
        
        # MinDate = ReferenceDate
        MinDate = GetDate(np.min([a.Arrival for a in self.Schedule]))

        #----------------------------------------
        # Set Data
        #----------------------------------------
        
        labels=[]
        for i in range(len(self.Schedule)):
            aircraft = self.Schedule[i]
            labels.append(aircraft.ID)
            color = aircraft.GetColor(Mode="GroundTime")
            t_a = (aircraft.Arrival  -MinDate).total_seconds()/3600.
            t_d = (aircraft.Departure-MinDate).total_seconds()/3600.
            dt = t_d-t_a
            ax.broken_barh([(t_a,dt)], (i-0.4,0.8), color=color)

        #----------------------------------------
        # Configure Plot
        #----------------------------------------
        
        plt.axvline(x=24*1) # Day line
        plt.axvline(x=24*2) # Day2 line

        #..............................
        # Labels
        #..............................
        
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels, fontsize=5) 
        ax.set_xlabel("Time [h]")

        #..............................
        # Layout
        #..............................
        
        plt.tight_layout()       
        if Show: plt.show(self.Airport.Name+": Schedule")

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Aircraft on Ground
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    def ShowAircraftOnGround(self,NrElements=int(24*(60/5.)),Show=True):

        fig,ax=plt.subplots(figsize=(16,9),dpi=120)

        #----------------------------------------
        # Set Data
        #----------------------------------------
        
        x = []
        y = []

        for i in range(NrElements*2):
            t = float(i)/NrElements * (3600*24)

            NrAircraft = 0
            for aircraft in self.Schedule:
                t_a = aircraft.Arrival_t
                t_d = aircraft.Departure_t
                if t_a<=t and t<=t_d:
                    NrAircraft+=1
                # print t/3600,t_a/3600,t_d/3600
            # print "t: "+str(round(    t/3600.,2))+" h","NrAircraft",NrAircraft
            x.append(t)
            y.append(NrAircraft)

        x = np.array(x)
        y = np.array(y) 
        NrAircraft_Max = np.max(y)

        color = [[float(na)/NrAircraft_Max,1-float(na)/NrAircraft_Max,0] for na in y]

        plt.bar(x/3600.,y,width=24./NrElements,color=color)

        #----------------------------------------
        # Configure Plot
        #----------------------------------------
        
        plt.axvline(x=24*1) # Day line
        plt.axvline(x=24*2) # Day2 line
        
        #..............................
        # Label
        #..............................
        
        plt.xlabel("Time [h]")
        plt.ylabel("Aircraft on ground [#]")

        #..............................
        # Layout
        #..............................
        
        plt.tight_layout()       
        if Show: plt.show(self.Airport.Name+": Aircraft on Ground")

#****************************************************************************************************
# Test Code
#****************************************************************************************************

if __name__=="__main__":
     
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Imports
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    from Airport import Airport

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Run Test
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    airport = Airport()
    airport.PrintInfo()

    SC = ScheduleCreator(airport)