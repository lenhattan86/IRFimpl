from resource import *
from user import *
from job import *

def DRF(capacity, isFDRF, users):
    # foreach user 
    demands = []
    normalizedDemands = []
    shares = []
    maxDemands = []

    dorminantRates = [0.0, 0.0, 0.0]
    for user in users:
    # convert to DRF or FDRF demands
        resDemand = Resource(0, 0, 0)
        normalizedDemand = [0.0, 0.0, 0.0]
        # print("user demand: "+ user.demand.toString() )
        if not isFDRF:
            if user.demand.beta > 1:
                resDemand.MilliCPU = 0.0
                resDemand.NvidiaGPU = float(user.demand.computation) / float(user.demand.beta) / 1000.0
                resDemand.Memory = 1.0 #user.demand.mem
            else:
                resDemand.MilliCPU = user.demand.computation 
                resDemand.NvidiaGPU = 0.0
                resDemand.Memory = user.demand.mem
        else:
            resDemand.MilliCPU = float(user.demand.computation)  / (1.0 + float(user.demand.beta))
            resDemand.NvidiaGPU = float(user.demand.computation)  / (1.0 + float(user.demand.beta)) /1000.0
            resDemand.Memory = user.demand.mem
        
        # print("resDemand: " + resDemand.toString())

        normalizedDemand[0] = float(resDemand.MilliCPU) / float(capacity.MilliCPU)
        normalizedDemand[1] = float(resDemand.Memory) / float(capacity.Memory)
        normalizedDemand[2] = float(resDemand.NvidiaGPU) / float(capacity.NvidiaGPU)   
        # print("normalized demand: " + str(normalizedDemand))

        demands.append(resDemand)   

        maxDemand = max(normalizedDemand)
        # print("max demand: " + str(maxDemand))
        maxDemands.append(maxDemand)

        dorminantRates[0] = dorminantRates[0] + normalizedDemand[0]/maxDemand
        dorminantRates[1] = dorminantRates[1] + normalizedDemand[1]/maxDemand
        dorminantRates[2] = dorminantRates[2] + normalizedDemand[2]/maxDemand

    # get total dorimant share for each all users
    dorminantShare = max(dorminantRates)
    # compute the share for each users
    borrowGPU = 0.0    
    for i in range(len(users)):
        
        ratio = dorminantShare * maxDemands[i]
        milliCPU = int(demands[i].MilliCPU  / ratio)        
        memory = int(demands[i].Memory  / ratio)        
        
        if(borrowGPU < -1):
            NvidiaGPU = round(demands[i].NvidiaGPU  / ratio)
            borrowGPU = borrowGPU +  round(demands[i].NvidiaGPU  / ratio) - (demands[i].NvidiaGPU  / ratio)
        else:
            NvidiaGPU = int(demands[i].NvidiaGPU  / ratio)
            borrowGPU = borrowGPU +  int(demands[i].NvidiaGPU  / ratio) - (demands[i].NvidiaGPU  / ratio)
        

        shares.append(Resource(milliCPU, memory, NvidiaGPU))

    # compute normalized demand
    return shares

###############################    
def enforceAllocation(share, jobs):    
    # cpu = share.MilliCPU
    # mem = share.Memory
    # gpu = share.NvidiaGPU

    maxTime = 0
    for job in jobs:
        maxTime = maxTime + max(job.cpuProfile.compl, job.gpuProfile.compl)

    runningJobs = {}
    # loggedJobs = {}
    loggedJobs = []
    for iTime in range(maxTime): 
        # compute current resource
        currentUsage = Resource(0, 0, 0)
        for jobId in runningJobs:
            runningJob = runningJobs[jobId]
            currentUsage.MilliCPU = currentUsage.MilliCPU + runningJob.usage.MilliCPU
            currentUsage.Memory = currentUsage.Memory + runningJob.usage.Memory
            currentUsage.NvidiaGPU = currentUsage.NvidiaGPU + runningJob.usage.NvidiaGPU            

        # allocate new jobs
        
        remainRes = substract(share, currentUsage)
        # print("Time" + str(iTime) + " currentUsage: " + currentUsage.toString() + " Remain: " + remainRes.toString())
        jobsTobeRemoved = []
        for job in jobs:
            jobProfile = job.fit(remainRes)            
            if jobProfile != None:
                # print("jobProfile.demand: " + jobProfile.demand.toString())
                activeJob = ActiveJob(jobProfile.demand, iTime, iTime + jobProfile.compl - 1, job.jobId, jobProfile.jobCmd)
                # print("remove job " + str(job.jobId))
                jobsTobeRemoved.append(job)
                runningJobs.update({job.jobId: activeJob})
                # loggedJobs.update({job.jobId: activeJob})
                loggedJobs.append(activeJob)
                remainRes = substract(remainRes, jobProfile.demand)

        # print(jobsTobeRemoved)
        for job in jobsTobeRemoved:  
            jobs.remove(job)

        # print("Time" + str(iTime) + " running jobs: "+ str(len(runningJobs)) + " remaining jobs: "+ str(len(jobs)) + " logged jobs: " + str(len(loggedJobs)))    

        # remove the finished jobs from the running jobs
        for jobId in runningJobs.keys():
            job = runningJobs[jobId]
            if job.endTime == iTime:
                runningJobs.pop(jobId)            
    
    return loggedJobs
    
def maxNormalizeDemand(normalizedDemand):
    
    maxDemand = 0.0
    if(maxDemand < normalizedDemand.MilliCPU):
        maxDemand = normalizedDemand.MilliCPU

    if(maxDemand < normalizedDemand.Memory):
        maxDemand = normalizedDemand.Memory

    if(maxDemand < normalizedDemand.NvidiaGPU):
        maxDemand = normalizedDemand.NvidiaGPU

    return maxDemand