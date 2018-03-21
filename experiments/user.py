from demand import *
from resource import *

class User:
    # list of jobs
    # username
    # demand    
    def __init__ (self, name, demand, jobs):
        self.username = name
        self.jobs = jobs
        self.demand = demand

    def getUsername(self):
        return self.username

    def createNormalizedDemand(self, nodeRes):
        self.normDemand = Demand(0.0,0.0,0.0)
        self.normDemand.computation = self.demand.computation/ nodeRes.MilliCPU
        self.normDemand.mem = self.demand.mem/ nodeRes.Memory
        self.normDemand.beta = self.demand.beta

    def toString(self):
        strUser = "username: " + self.username + "\n"        
        strUser = strUser+ "demand: " + self.demand.toString() + "\n"
        strUser = strUser +  "number of jobs: " + str(len(self.jobs))
        return strUser