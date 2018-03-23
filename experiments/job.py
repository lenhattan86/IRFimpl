from resource import *

class Job:    
    def __init__ (self, jobId, cpuProfile, gpuProfile, beta):
        self.cpuProfile = cpuProfile
        self.gpuProfile = gpuProfile
        self.beta = beta        
        self.jobId = jobId

    def fit(self, alloc):
        # print("gpuProfile: " + self.gpuProfile.toString())
        # print("cpuProfile: " + self.cpuProfile.toString())
        if self.gpuProfile.demand.isFit(alloc, True):
            return self.gpuProfile

        if self.cpuProfile.demand.isFit(alloc, False):
            return self.cpuProfile

        return None


class ActiveJob:
    def __init__ (self, usage, startTime, endTime, jobId, jobCmd):
        self.usage = usage
        self.startTime = startTime
        self.endTime = endTime
        self.jobId = jobId
        self.jobCmd = jobCmd

    def isFinished(self, currTime):
        if currTime >= self.endTime:
            return True
        return False

class JobProfile:
    def __init__(self, demand, compl, jobCmd):
        self.demand = demand
        self.compl = compl
        self.jobCmd = jobCmd

    def toString(self):    
        return "JobProfile: " + self.demand.toString() + " compl: " + str(self.compl)

JOB_LINES = 4
Gi = 1024*1024*1024
def readJobs(this_path, jobFile):    
    # try:
    f = open(this_path + '/' + jobFile)
    # except:
    #     print("cannot read file : " + this_path + '/' + jobFile)
    #     return []

    lines = f.readlines()
    jobs = []
    jobLineCount = 0
    jobId = 0
    for line in lines:
        strLine = line.strip()
        if not strLine.startswith("#"):   
            jobLineCount = jobLineCount + 1
            strArray = strLine.split()

            if(jobLineCount == 1):
                cCpu = int(strArray[0])
                cGPu = int(strArray[1]) # must be zero
                cMem = int(strArray[2]) * Gi
                cCompl = float(strArray[3])                

            elif(jobLineCount == 2):
                gCpu = int(strArray[0])
                gGPu = int(strArray[1])
                gMem = int(strArray[2]) * Gi
                gCompl = float(strArray[3])         
                
            elif(jobLineCount == 3):
                cpuCommand = strLine 

            elif(jobLineCount == JOB_LINES):     
                beta  = cCompl/gCompl           
                gpuCommand = strLine

                cpuDemand = Resource(cCpu, cMem, cGPu)
                cpuProfile = JobProfile(cpuDemand, cCompl, cpuCommand)

                gpuDemand = Resource(gCpu,  gMem, gGPu)
                gpuProfile = JobProfile(gpuDemand, gCompl, gpuCommand)

                job = Job(jobId, cpuProfile, gpuProfile, beta)
                jobs.append(job)
                jobId = jobId + 1
                
                jobLineCount = 0                

    f.close()
    return jobs