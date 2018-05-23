from resource import *

class JobInfo:    
    def __init__ (self, jobId, jobName, userName, numBatches):
        self.jobId = jobId
        self.jobName = jobName
        self.userName = userName
        self.starTime = -1
        self.stopTime = -1
        self.numBatches = numBatches
        self.complTime = -1
        self.estComplTime = -1
        self.estSpeedup = -1
        self.estCpuMemUsage = -1
        self.estGpuMemUsage = -1
        self.isFinished = False
        self.job = None