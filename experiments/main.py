import os 
this_path = os.path.dirname(os.path.realpath(__file__))

class User:
    # list of jobs
    # username
    # demand
    # beta
    def __init__ (self, name, beta, demand):
        self.username = name

    def getUsername(self):
        return self.username

class Demand:
    def __init__ (self, computation, mem, beta):
        self.computation = computation
        self.mem = mem
        self.beta = beta

class Resource:
    def __init__(self, MilliCPU, Memory, NvidiaGPU):
        self.MilliCPU = MilliCPU
        self.Memory = Memory
        self.NvidiaGPU = NvidiaGPU

class Job:
    def __init__ (self, jobId, demandObj):
        self.demand = demandObj
        self.jobId = jobId
        
def createDRFExperiement():
    print('DRF experiemnts')
     ## for DRF
    f = open(this_path +'/' + 'DRF_experiments.sh','w')
    f.write('dummy file')
    f.close()

def readJobs(jobFile):
    f = open(this_path + '/' + jobFile)
    lines = f.readlines()
    jobs = []
    isNewJob=true
    for line in lines: 
        if ~line.startswith("#"):
            print(line)
    f.close()

def main():
    print("Experiments for IRA")
    createDRFExperiement()
    ## for FDIRF

if __name__ == "__main__": main()