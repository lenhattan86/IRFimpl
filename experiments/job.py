from resource import *

class Job:    
    def __init__ (self, jobId, cpuProfile, gpuProfile, beta):
        self.cpuProfile = cpuProfile
        self.gpuProfile = gpuProfile
        self.beta = beta        
        self.jobId = jobId        
        tempArray = cpuProfile.jobCmd.split("--num_batches=")
        tempArray2 = gpuProfile.jobCmd.split("--num_batches=")
        if len(tempArray) == 2:            
            numBatches = int(tempArray[1])
            numBatches2 = int(tempArray2[1])
        else:
            print("[ERROR] command shoud have --num_batches= at the end")
        self.numBatches = numBatches
        self.numBatches2 = numBatches2

    def fit(self, alloc):
        # print("gpuProfile: " + self.gpuProfile.toString())
        # print("cpuProfile: " + self.cpuProfile.toString())
        result = []
        if self.gpuProfile.demand.isFit(alloc, True):
            result.append(self.gpuProfile)
            result.append(self.cpuProfile)
            return result

        if self.cpuProfile.demand.isFit(alloc, False):
            result.append(self.cpuProfile)
            result.append(self.gpuProfile)
            return result
        
        return result

    def jobProfiles(self):
        result = []
        result.append(self.gpuProfile)
        result.append(self.cpuProfile)
        return result

    def getBatchNum(self):
        print("TODO: fix job.getBatchNum(self)")
        return 100    


class ActiveJob:
    def __init__ (self, usage, secUsage, startTime, endTime, jobId, priJobCmd, seJobCmd, priComplt, secComplt):
        self.usage = usage
        self.secUsage = secUsage
        self.startTime = startTime
        self.endTime = endTime
        self.jobId = jobId
        self.jobCmd = priJobCmd
        self.seJobCmd = seJobCmd
        self.priComplt = priComplt
        self.secComplt = secComplt

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
def readJobs(this_path, jobFile, numRepJobs):    
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
    if numRepJobs > 0 and len(jobs)>0:
        mJob=jobs[0] 
        jobIdStart = len(jobs)       
        for i in range(0,numRepJobs-1):
            jobId  = jobIdStart + i
            newJob = Job(jobId, mJob.cpuProfile, mJob.gpuProfile, mJob.beta)
            jobs.append(newJob)

    f.close()
    return jobs