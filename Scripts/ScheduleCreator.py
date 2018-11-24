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

from Airlines      import AllAirlines
# from AircraftTypes import All_AircraftTypes
from ReferenceDate import ReferenceDate,GetDate

def getRoundedThreshold(a, MinClip):
    return np.round(float(a) / MinClip) * MinClip

#****************************************************************************************************
# ScheduleCreator
#****************************************************************************************************

class ScheduleCreator(object):
    """docstring for ScheduleCreator"""

    #================================================================================
    # Initialization
    #================================================================================
    
    def __init__(self, Airport,MaxNrAircraft=None,MaxNrOverlappingAircraft=30,Airlines=AllAirlines,ScheduleFolder="Temp",AutoRun=True):
        super(ScheduleCreator, self).__init__()

        self.Airport                  = Airport
        self.MaxNrAircraft            = MaxNrAircraft
        self.MaxNrOverlappingAircraft = MaxNrOverlappingAircraft
        self.Airlines            = Airlines

        self.ScheduleFolder = os.path.realpath(ScheduleFolder)
        if not os.path.exists(self.ScheduleFolder): os.makedirs(self.ScheduleFolder)

        if self.MaxNrAircraft is None:
            self.MaxNrAircraft = int((self.Airport.GetOperationalTime()/3600.)*self.MaxNrOverlappingAircraft*0.2)

        if AutoRun:
            self.Run()
        
    #================================================================================
    # Schedule Creator
    #================================================================================

    def Run(self,Print=True,Export=True,Visualize=True):

        self.CreateAircraftSchedule()
        if Print:     self.PrintSchedule()
        if Export:    self.ExportScheduleToExcel()
        if Visualize: self.Visualize()

    def CreateAircraftSchedule(self,TimeRange=[45*60,20*3600],MinTimeStep=5*60,Sort=True,dt0=ReferenceDate):

        self.Schedule = []

        dt0 = datetime.datetime(year=1900,month=1,day=1)

        BetaMean = np.mean([TimeRange[0]]*20+[TimeRange[1]])
        # print "BetaMean",BetaMean/3600.,"h"

        for i in range(self.MaxNrAircraft):

            #----------------------------------------
            # Airline
            #----------------------------------------
            
            airline = np.random.choice(self.Airlines)

            #----------------------------------------
            # AircraftType
            #----------------------------------------
            
            AircraftType = np.random.choice(airline.AircraftTypes)
            ID = i+1

            #----------------------------------------
            # Arrival/Departure
            #----------------------------------------
            
            #--- Arrival ---
            arrivalper = np.random.uniform()
            if 1:
                arrivalper = (arrivalper-0.5)*2 # Shift to [-1,+1]
                arrivalper = abs(arrivalper)**(1./1.4) * (abs(arrivalper)/arrivalper)      # Modulate
                arrivalper = (arrivalper+1)/2   # Reshift to [0,+1]
            ArrivalT   = (self.Airport.T_Open-dt0).total_seconds() + arrivalper * (self.Airport.T_Close-self.Airport.T_Open).total_seconds() # np.random.uniform((self.Airport.T_Open-dt0).total_seconds(),(self.Airport.T_Close-dt0).total_seconds())
            if MinTimeStep is not None: ArrivalT = getRoundedThreshold(ArrivalT,MinTimeStep)
            Arrival   = ReferenceDate + datetime.timedelta(seconds=ArrivalT)
            #--- GroundTime ---
            GroundTime = np.random.beta(2,5)/0.2*BetaMean# np.random.uniform(*TimeRange)
            if GroundTime<TimeRange[0]: GroundTime = TimeRange[0]
            if MinTimeStep is not None: GroundTime = getRoundedThreshold(GroundTime,MinTimeStep)
            #--- Departure ---
            Departure = Arrival       + datetime.timedelta(seconds=GroundTime)

            #----------------------------------------
            # Internal Properties
            #----------------------------------------
            
            #--- Nr Passengers ---
            NrPassenger_per = 1-np.random.beta(1,3)#(2,5)
            NrPassengers = int(AircraftType.MaxNrPassengers*NrPassenger_per)
            # print "NrPassengers:",NrPassengers

            #--- Domestic ---
            if np.random.uniform()<=0.75: Domestic = True
            else:                         Domestic = False 

            #--- Fueling ---
            if np.random.uniform()<=0.75: NeedsFueling = True
            else:                         NeedsFueling = False 

            #----------------------------------------
            # Create Aircraft
            #----------------------------------------
            
            a = AircraftType(ID=ID, Arrival=Arrival,Departure=Departure,NrPassengers=NrPassengers)
            a.Airline      = airline
            a.Domestic     = Domestic
            a.NeedsFueling = NeedsFueling

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
        ws.cell(row=1, column=3).value = "Airline"
        ws.cell(row=1, column=4).value = "Arrival"
        ws.cell(row=1, column=5).value = "Departure"
        ws.cell(row=1, column=6).value = "NrPassengers"
        ws.cell(row=1, column=7).value = "Domestic"
        ws.cell(row=1, column=8).value = "NeedsFueling"

        #----------------------------------------
        # Write Data
        #----------------------------------------

        for i in range(self.MaxNrAircraft):
            aircraft = self.Schedule[i]
            ws.cell(row=i+2, column=1).value = aircraft.ID
            ws.cell(row=i+2, column=2).value = aircraft.Type
            ws.cell(row=i+2, column=3).value = aircraft.Airline.Name
            ws.cell(row=i+2, column=4).value = aircraft.Arrival.time()
            ws.cell(row=i+2, column=5).value = aircraft.Departure.time()
            ws.cell(row=i+2, column=6).value = aircraft.NrPassengers
            ws.cell(row=i+2, column=7).value = aircraft.Domestic
            ws.cell(row=i+2, column=8).value = aircraft.NeedsFueling

        wb.save(os.path.join(self.ScheduleFolder,"Airport '"+str(self.Airport.Name)+"' - Schedule.xlsx"))

    #================================================================================
    # Visualize
    #================================================================================

    def Visualize(self,Show=False):
    
        self.ShowGanttChart(          Show=False)
        self.ShowAircraftOnGround(    Show=False)
        self.ShowAircraftGroundTime(  Show=False)
        self.ShowAircraftNrPassengers(Show=False)

        if Show: plt.show()

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
        title=self.Airport.Name+" - Schedule"
        plt.savefig(os.path.join(self.ScheduleFolder,title))
        if Show: plt.show(title)

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
        title = self.Airport.Name+" - Aircraft on Ground"
        plt.savefig(os.path.join(self.ScheduleFolder,title))
        if Show: plt.show(title)

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Aircraft GroundTime
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    def ShowAircraftGroundTime(self,Show=True):

        fig,ax=plt.subplots(figsize=(16,9),dpi=120)

        #----------------------------------------
        # Set Data
        #----------------------------------------
 
        GroundTimes = []
        for aircraft in self.Schedule:
            GroundTimes.append(aircraft.GroundTime/3600.)

        db = 0.5
        bins = np.arange(0,np.max(GroundTimes)+db, db) # None   
        plt.hist(GroundTimes,bins=bins)

        #----------------------------------------
        # Configure Plot
        #----------------------------------------
        
        #..............................
        # Label
        #..............................
        
        plt.xlabel("GroundTime [h]")
        plt.ylabel("Nr of Aircraft [#]")
        
        #..............................
        # Layout
        #..............................
        
        plt.tight_layout()
        title = self.Airport.Name+" - Aircraft GroundTime"
        plt.savefig(os.path.join(self.ScheduleFolder,title))
        if Show: plt.show(title)

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Aircraft GroundTime
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    def ShowAircraftNrPassengers(self,Show=True):

        fig,ax=plt.subplots(figsize=(16,9),dpi=120)

        #----------------------------------------
        # Set Data
        #----------------------------------------
 
        NrPassengers = []
        for aircraft in self.Schedule:
            NrPassengers.append(aircraft.NrPassengers)

        plt.hist(NrPassengers)

        #----------------------------------------
        # Configure Plot
        #----------------------------------------
        
        #..............................
        # Label
        #..............................
        
        plt.xlabel("NrPassengers [#]")
        plt.ylabel("Nr of Aircraft [#]")
        
        #..............................
        # Layout
        #..............................
        
        plt.tight_layout()
        title = self.Airport.Name+" - Aircraft NrPassengers"
        plt.savefig(os.path.join(self.ScheduleFolder,title))
        if Show: plt.show(title)

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