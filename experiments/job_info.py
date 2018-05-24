from resource import *

class JobInfo:    
    def __init__ (self, jobId, jobName, userName, numBatches):
        self.jobId = jobId
        self.jobName = jobName
        self.userName = userName
        self.starTime = -1
        self.starTimeGpu = -1
        self.stopTime = -1
        self.stopTimeGpu = -1
        self.numBatches = numBatches
        self.complTime = -1
        self.complTimeGpu = -1
        self.estComplTimeCpu = -1
        self.estComplTimeGpu = -1

        self.isEstimated=False
        self.estSpeedup = -1
        self.isComputed=False
        self.speedup = -1

        self.estCpuMemUsage = -1
        self.estGpuMemUsage = -1
        self.isFinished = False
        self.job = None
        self.isSubmitted=False
        self.isSubmittedGpu=False
        self.isGpuJob = False
        self.isSubmittedGpu = False
        