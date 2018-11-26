# -*- coding: utf-8 -*-
'''
Created on Tuesday 20.11.2018
Copyright (©) Henricus N. Basien
Author: Henricus N. Basien, Pavel Volkov
Email: Henricus@Basien.de
'''

#****************************************************************************************************
# ToDo
#****************************************************************************************************

"""
Objectives:
    (V) Walking Distances
    ( ) Towing
    ( ) Penalty
Constraints:
    (V) Bay Compliance
    (V) Bay Compatibility / Fueling
    (~) Night Stays
    (~) Domestic or International
    ( ) Adjacency
"""

#****************************************************************************************************
# Imports
#****************************************************************************************************

import os,sys
RootPath = os.path.split(__file__)[0]
sys.path.insert(0,os.path.join(RootPath,"Scripts"))

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# External
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from collections import OrderedDict

import pulp

from datetime import datetime
Now = datetime.now
from time import time as getTime
import numpy as np

import matplotlib.pyplot as plt

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Internal
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from ScheduleCreator import ScheduleCreator
from ReferenceDate import GetDate

#****************************************************************************************************
# GateAndBayAssignment
#****************************************************************************************************

class GateAndBayAssignmentSolver(object):
    """docstring for GateAndBayAssignmentSolver"""

    #================================================================================
    # Initialization
    #================================================================================
    
    def __init__(self, Airport,Schedule=None,LP_Path="Temp",LP_filepath=None,AutoRun=True):
        super(GateAndBayAssignmentSolver, self).__init__()
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Set Settings
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        self.Airport  = Airport
        self.Schedule = Schedule

        #--- LP ---
        self.LP_filepath = LP_filepath
        if self.LP_filepath is None:
            self.LP_Path = os.path.realpath(LP_Path)
        else:
            self.LP_Path = os.path.split(self.LP_filepath)[0]

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Schedule
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        if self.Schedule is None:
            MaxNrAircraft  = len(self.Airport.Bays)
            self.Scheduler = ScheduleCreator(self.Airport,MaxNrOverlappingAircraft=MaxNrAircraft,ScheduleFolder="Schedules",AutoRun=False)
            self.Scheduler.Run(Visualize=True)
            self.Schedule  = self.Scheduler.Schedule

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Run
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        if AutoRun:
            self.Run()
    #================================================================================
    # Run Assignment
    #================================================================================
    
    def Run(self,PrintProblem=False):

        print "*"*100
        print "Running LP Solver"
        print "*"*100

        t0 = getTime()

        if self.LP_filepath is None:
            self.CreateLP()
        self.ReconstructLP()
        if PrintProblem: print self.lp_problem
        self.RunLP()
        self.PrintResult()
        self.ExportResult()
        self.ConvertResult()

        dt = getTime()-t0
        print "+"*50
        print "Complete Problem solved @"+str(Now())+"\t in "+str(round(dt/60.,1))+" min"
        print "+"*50

        self.PlotResult()

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Create
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    def CreateLP(self):

        t0 = getTime()

        LP = []

        #--- Variables & Objectives ---
        LP+=self.GetLP_Variables()
        LP+=self.GetLP_ObjectiveFunctions()
        #--- Constaints ---
        LP+=self.GetLP_BayComplianceConstraints()
        LP+=self.GetLP_TimeConstraints()

        #..............................
        # Write to File
        #..............................
        
        if not os.path.exists(self.LP_Path): os.makedirs(self.LP_Path)
        self.LP_filepath = os.path.join(self.LP_Path,self.Airport.Name+" - GateAndBayAssignment.PuLP")
        with open(self.LP_filepath,"w") as LP_File:
            for line in LP:
                LP_File.write(line+"\n")

        dt = getTime()-t0
        print ">"*3+"Problem created       @"+str(Now())+"\t in "+str(round(dt,2))+"s"

    #----------------------------------------
    # Variables
    #----------------------------------------

    def GetLP_Variables(self):

        self.Variables = []
        
        for i in range(len(self.Schedule)):
            for k in range(len(self.Airport.Bays)):
                self.Variables.append("X_"+str(i)+"_"+str(k))
        
        Variables = ["Var: "+v for v in self.Variables]

        Variables.append("#"*100)

        return Variables

    #----------------------------------------
    # Objective Function(s)
    #----------------------------------------
    
    def GetLP_ObjectiveFunctions(self):

        # Objective function
        ObjectiveFunctions = []

        #..............................
        # Objective TransportDistance
        #..............................
    
        ObjectiveFunctions.append("# ObjectiveFunction - TransportDistance")
        ObjectiveFunctions.append("Var: Z1")

        ObjectiveFunction_TransportDistance = ""
        for i in range(len(self.Schedule)):
            a = self.Schedule[i]
            for k in range(len(self.Airport.Bays)):
                b = self.Airport.Bays[k]
                #--- Objective ---
                Terminal = a.Airline.Terminal
                GateName = b.Name
                if not (Terminal,GateName) in self.Airport.TravelDistances.keys():
                    GateName = GateName.rstrip("ABCD LR")
                TravelDistance = self.Airport.TravelDistances[(Terminal,GateName)]
                ObjectiveFunction_TransportDistance+= "X_"+str(i)+"_"+str(k)+"*"+str(a.NrPassengers)+"*"+str(TravelDistance)+ "+"
        ObjectiveFunction_TransportDistance+='0 == Z1'

        ObjectiveFunctions.append(ObjectiveFunction_TransportDistance)

        #..............................
        # Objective AirlinePreference
        #..............................
    
        ObjectiveFunctions.append("# ObjectiveFunction - AirlinePreference")
        ObjectiveFunctions.append("Var: Z2")

        ObjectiveFunction_AirlinePreference = ""
        for i in range(len(self.Schedule)):
            a = self.Schedule[i]
            for k in range(len(self.Airport.Bays)):
                if hasattr(a,"BayPreference") and a.BayPreference==k:
                    ObjectiveFunction_AirlinePreference+= "X_"+str(i)+"_"+str(k)+"*"+str(a.NrPassengers)+ "+"
        ObjectiveFunction_AirlinePreference+='0 == Z2'

        ObjectiveFunctions.append(ObjectiveFunction_AirlinePreference)

        #..............................
        # Objective RelocationPenalty
        #..............................
    
        ObjectiveFunctions.append("# ObjectiveFunction - RelocationPenalty")
        ObjectiveFunctions.append("Var: Z3")

        ObjectiveFunction_RelocationPenalty = ""
        # for i in range(len(self.Schedule)):
        #   a = self.Schedule[i]
        #   for k in range(len(self.Airport.Bays)):
        #       if hasattr(a,"BayPreference") and a.BayPreference==k:
        #           ObjectiveFunction_RelocationPenalty+= "X_"+str(i)+"_"+str(k)+"*"+str(a.NrPassengers)+ "+"
        ObjectiveFunction_RelocationPenalty+='0 == Z3'

        ObjectiveFunctions.append(ObjectiveFunction_RelocationPenalty)

        #..............................
        # Combine Objective
        #..............................
        
        ObjectiveFunctions.append("# ObjectiveFunction - Combined")

        Z1_Max = 1 # ToDo

        alpha = 1.0
        beta  = Z1_Max
        gamma = Z1_Max+2*beta
        ObjectiveFunctions.append(str(alpha)+'*Z1 + '+str(beta)+'*Z2 + '+str(gamma)+'*Z3 , "Z"')        

        #..............................
        # Addendum
        #..............................
        
        ObjectiveFunctions.append("#"*100)

        return ObjectiveFunctions

    #----------------------------------------
    # Constraints
    #----------------------------------------

    #..............................
    # Bay Compliance
    #..............................
    
    def GetLP_BayComplianceConstraints(self):

        BayComplianceConstraints = []

        BayComplianceConstraints.append("# BayCompliance Constraints")

        for i in range(len(self.Schedule)):
            BayComplianceConstraint = ""
            for k in range(len(self.Airport.Bays)):
                BayComplianceConstraint+="X_"+str(i)+"_"+str(k) + " + "
            BayComplianceConstraint+=" 0 == 1"
            BayComplianceConstraints.append(BayComplianceConstraint)

        return BayComplianceConstraints     

    #..............................
    # Time Constraints
    #..............................

    def GetLP_TimeConstraints(self):

        TimeConstraints = []

        TimeConstraints.append("# Time Constraints")

        for i in range(len(self.Schedule)):
            a1 = self.Schedule[i]
            for j in range(i,len(self.Schedule)):
                a2 = self.Schedule[j]
                #--- Avoid unrequired Constraints ---
                if i==j: continue
                if not self.ScheduleClash(a1,a2): continue
                #--- Cycle all Bays ---
                for k in range(len(self.Airport.Bays)):
                    TimeConstraints.append("X_"+str(i)+"_"+str(k) + " + " + "X_"+str(j)+"_"+str(k) + " <= 1")

        return TimeConstraints

    def ScheduleClash(self,a1,a2):
        #--- Base Constraints ---
        if   a1.Arrival  <a2.Departure and a1.Arrival  >a2.Arrival: return True
        elif a1.Departure<a2.Departure and a1.Departure>a2.Arrival: return True
        #--- Mirrored Constraints ---
        elif a2.Arrival  <a1.Departure and a2.Arrival  >a1.Arrival: return True
        elif a2.Departure<a1.Departure and a2.Departure>a1.Arrival: return True

        return False

    #----------------------------------------
    # Bay Compatibility
    #----------------------------------------
    
    def GetLP_BayCompatibilityConstraints(self):

        BayCompatibilityConstraints = []

        BayCompatibilityConstraints.append("# BayCompatibility Constraints")

        for i in range(len(self.Schedule)):
            a = self.Schedule[i]
            #--- Cycle all Bays ---
            for k in range(len(self.Airport.Bays)):
                b = self.Airport.Bays[i]
                if a.Type not in b.CompatibleAircraftTypes or (a.NeedsFueling and not b.FuelingPossible):
                    BayCompatibilityConstraints.append("X_"+str(i)+"_"+str(k)+" == 0")

        return BayCompatibilityConstraints

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Reconstruct
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def ReconstructLP(self):

        t0 = getTime()

        self.lp_problem = pulp.LpProblem("Gate&Bay Assignment Problem", pulp.LpMinimize)

        with open(self.LP_filepath) as LP_File:

            lines = LP_File.readlines()
            for line in lines:
                line = line.strip()
                if line=="" or line[0]=="#": continue

                #--- Add Variables ---
                if line[:4]=="Var:":
                    var = line[5:]
                    if var[0]=="Z":
                        VarType = "Continuous"
                    else:
                        VarType = "Binary"
                    exec(var+" = pulp.LpVariable('"+var+"', cat='"+VarType+"')")
                    continue
                #--- Add Constraints ---
                exec("self.lp_problem+="+line)

        dt = getTime()-t0
        print ">"*3+"Problem reconstructed @"+str(Now())+"\t in "+str(round(dt,2))+"s"

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Run 
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def RunLP(self):

        t0 = getTime()

        self.lp_problem.solve()

        dt = getTime()-t0
        print ">"*3+"Problem solved        @"+str(Now())+"\t in "+str(round(dt,2))+"s"

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Print
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    def PrintResult(self,ShowVariables=False):

        print "*"*100

        #----------------------------------------
        # Variables
        #----------------------------------------
        
        if ShowVariables:
            print "Variables:"

            for variable in self.lp_problem.variables():
                print " "*3+"{} = {}".format(variable.name, variable.varValue)

        #----------------------------------------
        # Status
        #----------------------------------------
        
        print "Status: "+str(pulp.LpStatus[self.lp_problem.status])

        #----------------------------------------
        # Objective
        #----------------------------------------
        
        print "Objective:"
        print " "*3+str(pulp.value(self.lp_problem.objective))

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Export
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    def ExportResult(self):

        with open(os.path.join(self.LP_Path,"LP_result.txt"),"w") as ResultsFile:
            for variable in self.lp_problem.variables():
                ResultsFile.write("{} = {}".format(variable.name, variable.varValue)+"\n")

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Convert Result
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
    def ConvertResult(self,PrintResult=True):

        self.BayAssignment      = OrderedDict()
        self.BayAssignment_Dual = OrderedDict()

        for variable in self.lp_problem.variables():
            if variable.varValue==0: continue
            if variable.name[0]=="Z": continue
            X,i,k = variable.name.split("_")
            i = int(i);k = int(k)

            K = str(k)
            self.BayAssignment[self.Schedule[i].ID] = self.Airport.Bays[k]
            #--- Dual ---
            if not K in self.BayAssignment_Dual:
                self.BayAssignment_Dual[K] = []
            self.BayAssignment_Dual[K].append(self.Schedule[i])

        #--- Sort ---
        self.BayAssignment_Dual = OrderedDict(sorted(self.BayAssignment_Dual.items(), key=lambda t: t[0]))

        #--- Print ---
        if PrintResult:
            for key in self.BayAssignment.keys():
                print key,self.BayAssignment[key]

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Plot Result
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    def PlotResult(self,fontsize=4,Show=True):

        if Show:
            plt.close('all')

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
        for k in range(len(self.Airport.Bays)):
            #--- Add Labels ---
            Bay = self.Airport.Bays[k]
            labels.append(str(Bay))
            #--- Check Use ---
            K = str(k)
            if not K in self.BayAssignment_Dual.keys(): continue
            for aircraft in self.BayAssignment_Dual[K]:
                # color = None
                t_a = (aircraft.Arrival  -MinDate).total_seconds()/3600.
                t_d = (aircraft.Departure-MinDate).total_seconds()/3600.
                dt = t_d-t_a
                ax.broken_barh([(t_a,dt)], (k-0.4,0.8))

                if 1:
                    ax.annotate(aircraft.Type+" - ID: "+aircraft.ID+"\n"+"> #P: "+str(aircraft.NrPassengers), (t_a,k),
                    fontsize=fontsize,
                    horizontalalignment='left', verticalalignment='center')

        #----------------------------------------
        # Configure Plot
        #----------------------------------------
        
        self.Scheduler.ShowAirportDayLines()

        #..............................
        # Labels
        #..............................
        
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels, fontsize=fontsize) 
        ax.set_xlabel("Time [h]")

        #..............................
        # Layout
        #..............................
        
        plt.xlim(left=0)
        plt.tight_layout()
        title=self.Airport.Name+" - Bay Assignment"
        plt.savefig(os.path.join(self.Scheduler.ScheduleFolder,title))
        if Show:
            plt.show(title)

#****************************************************************************************************
# Test Code
#****************************************************************************************************

if __name__=="__main__":

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Imports
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    from JKIA import JKIA

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Run Test
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    airport = JKIA()
    airport.PrintInfo()

    GABA_Solver = GateAndBayAssignmentSolver(airport)
