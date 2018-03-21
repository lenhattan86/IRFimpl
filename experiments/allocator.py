from resource import *
from user import *
from job import *

def DRF(capacity, isFDRF, users, cpu2gpuRatio):
    # foreach user 
    demands = []
    normalizedDemands = []
    shares = []
    computedShares = []
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
                resDemand.NvidiaGPU = float(user.demand.computation) / float(user.demand.beta) / cpu2gpuRatio
                resDemand.Memory = user.demand.mem
            else:
                resDemand.MilliCPU = user.demand.computation 
                resDemand.NvidiaGPU = 0.0
                resDemand.Memory = user.demand.mem
        else:
            resDemand.MilliCPU = float(user.demand.computation) / (1.0 + float(user.demand.beta))
            resDemand.NvidiaGPU = float(user.demand.computation)  / (1.0 + float(user.demand.beta)) / cpu2gpuRatio 
            resDemand.Memory = user.demand.mem
        
        # print("resDemand: " + resDemand.toString())

        normalizedDemand[0] = float(resDemand.MilliCPU) / float(capacity.MilliCPU)
        normalizedDemand[1] = float(resDemand.Memory) / float(capacity.Memory)
        normalizedDemand[2] = float(resDemand.NvidiaGPU) / float(capacity.NvidiaGPU)   
        print("normalized demand: " + str(normalizedDemand))

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
        NvidiaGPU = int(demands[i].NvidiaGPU  / ratio)
        # if(borrowGPU < -1):
        #     NvidiaGPU = round(demands[i].NvidiaGPU  / ratio)
        #     borrowGPU = borrowGPU +  round(demands[i].NvidiaGPU  / ratio) - (demands[i].NvidiaGPU  / ratio)
        # else:
        #     NvidiaGPU = int(demands[i].NvidiaGPU  / ratio)
        #     borrowGPU = borrowGPU +  int(demands[i].NvidiaGPU  / ratio) - (demands[i].NvidiaGPU  / ratio)
        

        shares.append(Resource(milliCPU, memory, NvidiaGPU))
        computedShares.append(Resource(demands[i].MilliCPU  / ratio, demands[i].Memory  / ratio, demands[i].NvidiaGPU  / ratio))

    # compute normalized demand
    printShares(computedShares)
    return shares


def ES(capacity, users):
    shares = []
    computedShares = []
    N = len(users)
    for user in users:
        milliCPU = int(capacity.MilliCPU  / N)        
        memory = int(capacity.Memory  / N)        
        NvidiaGPU = int(capacity.NvidiaGPU  / N)

        shares.append(Resource(milliCPU, memory, NvidiaGPU))
        computedShares.append(Resource(capacity.MilliCPU  / N, capacity.Memory  / N, capacity.NvidiaGPU  / N))

    # compute normalized demand
    printShares(computedShares)
    return shares


def Pricing(capacity, isFDRF, users, baseRes):
    shares = []
    N = len(users)
    # step 1: sort users based on beta (ascending)
    users.sort(key=lambda x: x.demand.beta, reverse=False)
    # step 2: compute the ratios
    ratios = []
    betas = []
    for user in users:
        ratio = user.demand.mem / user.demand.computation / ( baseRes.Memory / baseRes.MilliCPU) # normalized ratio 
        ratios.append(ratio)
        betas.append(user.demand.beta)

    # step 3: initialization
    price = [0, 0, 0] # prices on each resource.
    price[0] = 1 # for cpu
    price[1] = users[N-1].demand.beta # for gpu
    price[2] = 1 + users[N-1].demand.beta # for memory
    useralloc = userallocGPU(betas, ratios, price)

    currLoad = sumResource(useralloc) # normalized load
    gpumin = N - 1
    flag = True
    
    finalAlloc = []
    if(currLoad.NvidiaGPU > currLoad.MilliCPU):
        finalAlloc = useralloc
        finalAlloc[N-1].MilliCPU = 0
        finalAlloc[N-1].NvidiaGPU = 0
        currLoad = sumResource(finalAlloc)

        finalAlloc[N-1].NvidiaGPU = (currLoad.MilliCPU - currLoad.NvidiaGPU + (finalAlloc[N-1].Memory/ratios[N-1])) / (1 + betas[N-1])
        finalAlloc[N-1].MilliCPU = (currLoad.NvidiaGPU - currLoad.Memory + (finalAlloc[N-1].Memory/ratios[N-1])) / (1 + betas[N-1])
        currLoad = sumResource(finalAlloc)

    
    if N == 0:
        return shares
    elif N ==1:
        finalAlloc.append(capacity)

    # step 4: pricing
    error = 0.0001
    while (abs(currLoad.MilliCPU - currLoad.NvidiaGPU) > error and flag):
        gpumin = gpumin -1 
        if(gpumin < 0):
            print("###gpumin is negative####")
        price[0] = 1
        price[1] = betas[gpumin]
        price[2] = 1 + betas[gpumin]

    # step 5: create the real shares.
    for user in users:
        print("beta: " + str(user.demand.beta))
        ratio= 1
        milliCPU = int(capacity.MilliCPU  / ratio)        
        memory = int(capacity.Memory  / ratio)        
        NvidiaGPU = int(capacity.NvidiaGPU  / ratio)
        shares.append(Resource(milliCPU, memory, NvidiaGPU))

    return shares


def userallocGPU(betas, ratios, currentPrices):
    userAlloc = [] 

    for j in range(betas):
        beta = betas[j]
        ratio = ratios[j]
        alloc = Resource(0, 0, 0)
        alloc.Memory = min(1 / currentPrices[2], max(ratio, beta * ratio/currentPrices[1]))

        if (beta < currentPrices[1]) :
            alloc.MilliCPU = userAlloc[j].resource(2) / ratio
            alloc.NvidiaGPU = 0
        else: # if beta = price, put it in GPU.
            alloc.MilliCPU = 0
            alloc.NvidiaGPU = alloc.MilliCPU/(ratio*beta)
        userAlloc.append(alloc)

    return userAlloc   
    
def printShares(shares):
    strShares = "{"
    for share in shares:
        strShares = strShares + share.toString() + ","
    strShares = strShares + "}"
    print(strShares)

##############################################

def enforceAllocation(share, jobs, stopTime):    
    # cpu = share.MilliCPU
    # mem = share.Memory
    # gpu = share.NvidiaGPU

    maxTime = 0
    for job in jobs:
        maxTime = maxTime + max(job.cpuProfile.compl, job.gpuProfile.compl)

    runningJobs = {}
    # loggedJobs = {}
    loggedJobs = []
    # for iTime in range(maxTime): 
    for iTime in range(stopTime):
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