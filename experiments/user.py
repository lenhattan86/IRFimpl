from demand import *

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

    def toString(self):
        strUser = "username: " + self.username + "\n"        
        strUser = strUser+ "demand: " + self.demand.toString() + "\n"
        strUser = strUser +  "number of jobs: " + str(len(self.jobs))
        return strUser