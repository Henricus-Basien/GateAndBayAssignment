# -*- coding: utf-8 -*-
'''
Created on Tuesday 20.11.2018
Copyright (©) Henricus N. Basien
Author: Henricus N. Basien, Pavel Volkov
Email: Henricus@Basien.de
'''

#****************************************************************************************************
# Imports
#****************************************************************************************************

import os,sys
RootPath = os.path.split(__file__)[0]
sys.path.insert(0,os.path.join(RootPath,"Scripts"))

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# External
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from time import time as getTime

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Internal
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from ScheduleCreator import ScheduleCreator
import pulp

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
		#--- Set Settings ---
		self.Airport  = Airport
		self.Schedule = Schedule

		self.LP_filepath = LP_filepath
		if self.LP_filepath is None:
			self.LP_Path = os.path.realpath(LP_Path)
		else:
			self.LP_Path = os.path.split(self.LP_filepath)[0]

		#--- Schedule ---
		if self.Schedule is None:
			MaxNrAircraft  = len(self.Airport.Bays)
			self.Scheduler = ScheduleCreator(self.Airport,MaxNrOverlappingAircraft=MaxNrAircraft,ScheduleFolder="Schedules",AutoRun=False)
			self.Scheduler.Run(Visualize=True)
			self.Schedule  = self.Scheduler.Schedule

		#--- Run ---
		if AutoRun:
			self.Run()

	#================================================================================
	# Run Assignment
	#================================================================================
	
	def Run(self,PrintProblem=False):

		print "*"*100
		print "Running LP Solver"
		print "*"*100

		if self.LP_filepath is None:
			self.CreateLP()
		self.ReconstructLP()
		if PrintProblem: print self.lp_problem
		self.RunLP()
		self.PrintResult()
		self.ExportResult()

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
		self.LP_filepath = os.path.join(self.LP_Path,"LP.txt")
		with open(self.LP_filepath,"w") as LP_File:
			for line in LP:
				LP_File.write(line+"\n")

		dt = getTime()-t0
		print ">"*3+"Problem created       in "+str(round(dt,2))+"s"

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
		ObjectiveFunctions_ = []

		#ObjectiveFunctions_ += ['4 * x + 3 * y, "Z"']

		#..............................
		# Objective #1
		#..............................
	
		ObjectiveFunction_1 = ""

		for i in range(len(self.Schedule)):
			a = self.Schedule[i]
			for k in range(len(self.Airport.Bays)):
				ObjectiveFunction_1+= "X_"+str(i)+"_"+str(k)+"*"+str(a.NrPassengers)+ "+"
		ObjectiveFunction_1+='0 , "Z"'

		ObjectiveFunctions_.append(ObjectiveFunction_1)

		#..............................
		# Append Objectives
		#..............................
		
		ObjectiveFunctions = []

		for i in range(len(ObjectiveFunctions_)):
			ObjectiveFunctions.append("# ObjectiveFunction Nr."+str(i+1))
			ObjectiveFunctions.append(ObjectiveFunctions_[i])

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
			for j in range(len(self.Schedule)):
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

	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	# Reconstruct
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	def ReconstructLP(self):

		t0 = getTime()

		self.lp_problem = pulp.LpProblem("Gate&Bay Assignment Problem", pulp.LpMaximize)

		with open(self.LP_filepath) as LP_File:

			lines = LP_File.readlines()
			for line in lines:
				line = line.strip()
				if line=="" or line[0]=="#": continue

				#--- Add Variables ---
				if line[:4]=="Var:":
					var = line[5:]
					exec(var+" = pulp.LpVariable('"+var+"', cat='Binary')")
					continue
				#--- Add Constraints ---
				exec("self.lp_problem+="+line)

		dt = getTime()-t0
		print ">"*3+"Problem reconstructed in "+str(round(dt,2))+"s"

	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	# Run 
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	def RunLP(self):

		t0 = getTime()

		self.lp_problem.solve()

		dt = getTime()-t0
		print ">"*3+"Problem solved        in "+str(round(dt,2))+"s"

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
