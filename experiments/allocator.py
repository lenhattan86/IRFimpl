from resource import *
from user import *
from job import *

MILLI = 1000
GI = 1024*1024*1024

def devide(array, maxVal):
    for i in range(len(array)):
        array[i] = array[i]/maxVal
    return array

def FDRF(capacity, users):
    # foreach user 
    shares = []    
    dorminantRates = [0.0, 0.0, 0.0]
    proportions = []
    for user in users:
    # convert to DRF or FDRF demands
        proportion = [1.0, 1.0, 1.0]
        proportion[2] = float(capacity.MilliCPU/user.demand.computation + capacity.NvidiaGPU/user.demand.gpu)/float(capacity.Memory)*user.demand.mem
        maxProportion = max(proportion)
        proportion = devide(proportion, maxProportion)
        # maxDemands.append(proportion)
        for i in range(len(dorminantRates)):
            dorminantRates[i] = dorminantRates[i] + proportion[i] 
        proportions.append(proportion)

    # get total dorimant share for each all users
    dorminantShare = max(dorminantRates)    
    # compute the share for each users
    for i in range(len(users)):
        proportion = proportions[i]
        ratio = devide(proportion,dorminantShare)
        milliCPU = int(ratio[0]*capacity.MilliCPU )
        NvidiaGPU = int(ratio[1] * capacity.NvidiaGPU)
        memory = int(ratio[2]*capacity.Memory)
        ## convert to 
        shares.append(Resource(milliCPU, memory, NvidiaGPU))

    # compute normalized demand
    return shares

def DRF_old(capacity, isFDRF, users):
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
            if user.demand.beta >= 1:
                resDemand.MilliCPU = 0.0
                resDemand.NvidiaGPU = float(user.demand.computation) / float(user.demand.beta) 
                resDemand.Memory = user.demand.mem
            else:
                resDemand.MilliCPU = user.demand.computation 
                resDemand.NvidiaGPU = 0.0
                resDemand.Memory = user.demand.mem
        else:
            resDemand.MilliCPU = float(user.demand.computation) / (1.0 + float(user.demand.beta))
            resDemand.NvidiaGPU = float(user.demand.computation)  / (1.0 + float(user.demand.beta)) 
            resDemand.Memory = user.demand.mem
        
        # print("resDemand: " + resDemand.toString())

        normalizedDemand[0] = float(resDemand.MilliCPU) 
        normalizedDemand[1] = float(resDemand.Memory) 
        normalizedDemand[2] = float(resDemand.NvidiaGPU) 
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
    for i in range(len(users)):
        ratio = dorminantShare * maxDemands[i]
        milliCPU = int(demands[i].MilliCPU  / ratio*capacity.MilliCPU )
        memory = int(demands[i].Memory  / ratio*capacity.Memory)
        NvidiaGPU = int(demands[i].NvidiaGPU  / ratio * capacity.NvidiaGPU)

        ## convert to 
        shares.append(Resource(milliCPU, memory, NvidiaGPU))

    # compute normalized demand
    return shares


def naiveDRF(capacity, isFDRF, users, demands):
    # foreach user 
    shares = []
    computedShares = []
    maxDemands = []
    dorminantRates = [0.0, 0.0, 0.0]
    for i in range(len(users)):
    # convert to DRF or FDRF demands
        resDemand = demands[i]
        normalizedDemand = [0.0, 0.0, 0.0]
        
        normalizedDemand[0] = float(resDemand.MilliCPU)/capacity.MilliCPU 
        normalizedDemand[1] = float(resDemand.Memory)  /capacity.Memory 
        normalizedDemand[2] = float(resDemand.NvidiaGPU) /capacity.NvidiaGPU
        # print("normalized demand: " + str(normalizedDemand))

        maxDemand = max(normalizedDemand)
        # print("max demand: " + str(maxDemand))
        maxDemands.append(maxDemand)

        dorminantRates[0] = dorminantRates[0] + normalizedDemand[0]/maxDemand
        dorminantRates[1] = dorminantRates[1] + normalizedDemand[1]/maxDemand
        dorminantRates[2] = dorminantRates[2] + normalizedDemand[2]/maxDemand

    # get total dorimant share for each all users
    dorminantShare = max(dorminantRates)

    # compute the share for each users
    for i in range(len(users)):
        ratio = dorminantShare * maxDemands[i]
        milliCPU = int(demands[i].MilliCPU  / ratio )
        memory = int(demands[i].Memory  / ratio )
        NvidiaGPU = int(demands[i].NvidiaGPU  / ratio)

        shares.append(Resource(milliCPU, memory, NvidiaGPU))
        # computedShares.append(Resource(demands[i].MilliCPU  / ratio, demands[i].Memory  / ratio, demands[i].NvidiaGPU  / ratio))

    # compute normalized demand
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

def Static(capacity, users):
    shares = []
    
    # user 1
    milliCPU = int(2*MILLI)        
    memory = int(24*GI)        
    NvidiaGPU = int(2)    
    shares.append(Resource(milliCPU, memory, NvidiaGPU))

    # user2        
    milliCPU = int(86*MILLI)        
    memory = int(116*GI)    
    NvidiaGPU = 2

    shares.append(Resource(milliCPU, memory, NvidiaGPU))

    return shares

def Static2(capacity, users):
    shares = []
    
    # user 1
    milliCPU = int(86*MILLI)        
    memory = int(116*GI)    
    NvidiaGPU = 2  
    shares.append(Resource(milliCPU, memory, NvidiaGPU))

    # user2
    milliCPU = int(2*MILLI)        
    memory = int(24*GI)        
    NvidiaGPU = int(2)  
    shares.append(Resource(milliCPU, memory, NvidiaGPU))

    return shares

def allox(capacity, users):
    shares = []
    N = len(users)
    # step 1: sort users based on beta (ascending)
    users.sort(key=lambda x: x.demand.beta, reverse=False)
    # step 2: compute the ratios
    ratios = []
    betas = []
    for user in users:
        ratio = user.demand.mem / user.demand.computation  # normalized ratio 
        ratios.append(ratio)
        # normalize beta
        beta = user.demand.beta
        betas.append(beta)

    # step 3: initialization
    gpumin = N-1
    price = [0, 0, 0] # prices on CPU & GPU.
    price[0] = 1 # for cpu    
    price[1] = betas[gpumin] # for gpu    
    useralloc = userAlloc(betas, price)
    currLoad = sumResourceNorm(useralloc, capacity) # normalized load
    prevLoad = currLoad
    prevUserAlloc = useralloc

    finalAlloc = []
    
    if N == 0:
        return shares
    elif N ==1:
        finalAlloc.append(capacity)

    # step 4: pricing
    
    while (True):
        if (currLoad.MilliCPU <= currLoad.NvidiaGPU):   
            # method 1: using the previous allocation and balance it.
            # useralloc = prevUserAlloc            
            # useralloc[gpumin].MilliCPU  = useralloc[gpumin].MilliCPU - (prevLoad.MilliCPU - prevLoad.NvidiaGPU)*capacity.MilliCPU/2
            # useralloc[gpumin].NvidiaGPU = useralloc[gpumin].NvidiaGPU + (prevLoad.MilliCPU - prevLoad.NvidiaGPU)*capacity.NvidiaGPU/2

            # method 2: using the current allocation and balance it.
            # useralloc[gpumin].MilliCPU  = useralloc[gpumin].MilliCPU  + (currLoad.NvidiaGPU - currLoad.MilliCPU)*capacity.MilliCPU/2
            # useralloc[gpumin].NvidiaGPU = useralloc[gpumin].NvidiaGPU - (currLoad.NvidiaGPU - currLoad.MilliCPU)*capacity.NvidiaGPU/2
            
            # method 3: using the last allocation for others. find out the allocatino for gpumin      
            userallocCPU =  userAllocCPU(betas, price)  
            cpuCurrLoad =  sumResourceNorm(userallocCPU, capacity)
            useralloc[gpumin].MilliCPU  = abs(cpuCurrLoad.MilliCPU - currLoad.NvidiaGPU)/2*capacity.MilliCPU
            useralloc[gpumin].NvidiaGPU = abs(cpuCurrLoad.MilliCPU - currLoad.NvidiaGPU)/2*capacity.NvidiaGPU
            currLoad = sumResourceNorm(useralloc, capacity)
            break

        gpumin = gpumin -1 
        if(gpumin < 0):
            print("###gpumin is negative####")
            break
        price[0] = 1
        price[1] = betas[gpumin]
        prevUserAlloc = useralloc 
        prevLoad = currLoad
        useralloc = userAlloc(betas, price)                    
        currLoad = sumResourceNorm(useralloc, capacity)  

    finalAlloc = useralloc

    if (N > 1) :
        sumAlloc = sumResource(finalAlloc)

    # step 5: create the real shares.
    for i in range(N):
        cpu = finalAlloc[i].MilliCPU * capacity.MilliCPU / sumAlloc.MilliCPU
        gpu = round(finalAlloc[i].NvidiaGPU * capacity.NvidiaGPU / sumAlloc.NvidiaGPU)
        # gpu = finalAlloc[i].NvidiaGPU * capacity.NvidiaGPU / sumAlloc.NvidiaGPU
        mem = cpu / users[i].demand.computation * users[i].demand.mem + gpu / users[i].demand.gpu * users[i].demand.gpu_mem
        shares.append(Resource(int(cpu), int(mem), gpu))

    return shares    

def allox_bk(capacity, users):
    shares = []
    N = len(users)
    # step 1: sort users based on beta (ascending)
    users.sort(key=lambda x: x.demand.beta, reverse=False)
    # step 2: compute the ratios
    ratios = []
    betas = []
    for user in users:
        ratio = user.demand.mem / user.demand.computation  # normalized ratio 
        ratios.append(ratio)
        # normalize beta
        beta = user.demand.beta
        betas.append(beta)

    # step 3: initialization
    gpumin = N-1
    price = [0, 0, 0] # prices on CPU & GPU.
    price[0] = 1 # for cpu    
    price[1] = betas[gpumin] # for gpu    
    useralloc = userAlloc(betas, price)
    currLoad = sumNormalizedLoads(betas,useralloc) # normalized load
   
    finalAlloc = []
    
    if N == 0:
        return shares
    elif N ==1:
        finalAlloc.append(capacity)

    # step 4: pricing
    
    while (True):
        if (currLoad.MilliCPU <= currLoad.NvidiaGPU):            
            useralloc[gpumin].MilliCPU  = useralloc[gpumin].MilliCPU + (currLoad.NvidiaGPU - currLoad.MilliCPU)/2
            useralloc[gpumin].NvidiaGPU = useralloc[gpumin].NvidiaGPU - (currLoad.NvidiaGPU - currLoad.MilliCPU)/2/betas[gpumin]
            # currLoad = sumNormalizedLoads(betas,useralloc)
            break

        gpumin = gpumin -1 
        if(gpumin < 0):
            print("###gpumin is negative####")
            break
        price[0] = 1
        price[1] = betas[gpumin]
        useralloc = userAlloc(betas, price)        
        currLoad = sumNormalizedLoads(betas,useralloc)  

    finalAlloc = useralloc

    if (N > 1) :
        sumAlloc = sumResource(finalAlloc)


    # step 5: create the real shares.
    for i in range(N):
        cpu = finalAlloc[i].MilliCPU * capacity.MilliCPU / sumAlloc.MilliCPU
        gpu = finalAlloc[i].NvidiaGPU * capacity.NvidiaGPU / sumAlloc.NvidiaGPU
        mem = finalAlloc[i].Memory * capacity.Memory
        shares.append(Resource(int(cpu), int(mem), round(gpu)))

    return shares    


def userAlloc(betas, currentPrices):
    userAlloc = [] 

    for j in range(len(betas)):
        beta = betas[j]
        alloc = Resource(0, 0, 0)
        if (beta < currentPrices[1]) :
            alloc.MilliCPU = 1
            alloc.NvidiaGPU = 0
        else: # if beta = price, put it in GPU.
            alloc.MilliCPU = 0
            alloc.NvidiaGPU = 1/currentPrices[1]
        userAlloc.append(alloc)

    return userAlloc 


def userAllocCPU(betas, currentPrices):
    userAlloc = [] 
    for j in range(len(betas)):
        beta = betas[j]
        alloc = Resource(0, 0, 0)
        if (beta <= currentPrices[1]) : # if beta = price, put it in CPU.
            alloc.MilliCPU = 1
            alloc.NvidiaGPU = 0
        else: 
            alloc.MilliCPU = 0
            alloc.NvidiaGPU = 1/currentPrices[1]
        userAlloc.append(alloc)

    return userAlloc 

    
def printShares(shares):
    strShares = "{"
    for share in shares:
        strShares = strShares + share.toString() + ","
    strShares = strShares + "}"
    print(strShares)

##############################################

def toActiveJobs(jobs):    
    loggedJobs = []
    # for iTime in range(maxTime): 
    for job in jobs:
        defaultJobProfiles = job.jobProfiles()
        jobProfile = defaultJobProfiles[0]
        secProfile = defaultJobProfiles[1]
        activeJob = ActiveJob(jobProfile.demand, secProfile.demand, 0, 0 , job.jobId, jobProfile.jobCmd, secProfile.jobCmd)
        loggedJobs.append(activeJob)
            
    return loggedJobs

def enforceAllocation(share, jobs, stopTime, isBestFit):    
    # cpu = share.MilliCPU
    # mem = share.Memory
    # gpu = share.NvidiaGPU
    maxTime = 0
    for job in jobs:
        maxTime = maxTime + max(job.cpuProfile.compl, job.gpuProfile.compl)

    runningJobs = {}
    # loggedJobs = {}
    loggedJobs = []
    numOfJobs = 0
    # for iTime in range(maxTime): 
    for iTime in range(stopTime):
        # compute current resource
        currentUsage = Resource(0, 0, 0)
        for jobId in runningJobs:
            runningJob = runningJobs[jobId]
            if runningJob.usage.NvidiaGPU == 0: # ignore the cpu overhead for GPU jobs               
                currentUsage.MilliCPU = currentUsage.MilliCPU + runningJob.usage.MilliCPU
            currentUsage.Memory = currentUsage.Memory + runningJob.usage.Memory
            currentUsage.NvidiaGPU = currentUsage.NvidiaGPU + runningJob.usage.NvidiaGPU            

        # allocate new jobs
        remainRes = substract(share, currentUsage)
        # print("Time" + str(iTime) + " currentUsage: " + currentUsage.toString() + " Remain: " + remainRes.toString())
        jobsTobeRemoved = []
        for job in jobs:
            bestFitJobProfiles = job.fit(remainRes)
            defaultJobProfiles = job.jobProfiles()
            
            if len(bestFitJobProfiles)>0:
                jobProfile = bestFitJobProfiles[0]
                secProfile = bestFitJobProfiles[1]
                # print("jobProfile.demand: " + jobProfile.demand.toString())
                activeJob = ActiveJob(jobProfile.demand,secProfile.demand, iTime, iTime + jobProfile.compl - 1, job.jobId, jobProfile.jobCmd, secProfile.jobCmd)
                # print("remove job " + str(job.jobId))
                jobsTobeRemoved.append(job)
                runningJobs.update({job.jobId: activeJob})
                # loggedJobs.update({job.jobId: activeJob})

                if isBestFit:
                    loggedJobs.append(activeJob)
                else:
                    defaultJob = ActiveJob(defaultJobProfiles[0].demand,defaultJobProfiles[1].demand, iTime, iTime + jobProfile.compl - 1, 
                            job.jobId, defaultJobProfiles[0].jobCmd, defaultJobProfiles[1].jobCmd)
                    loggedJobs.append(defaultJob)
                
                remainRes = substract(remainRes, jobProfile.demand)

        # print(jobsTobeRemoved)
        for job in jobsTobeRemoved:  
            jobs.remove(job)

        # print("Time" + str(iTime) + " running jobs: "+ str(len(runningJobs)) + " remaining jobs: "+ str(len(jobs)) + " logged jobs: " + str(len(loggedJobs)))    

        # remove the finished jobs from the running jobs
        for jobId in runningJobs.keys():
            job = runningJobs[jobId]
            if iTime >= job.endTime:
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


def Pricing(capacity, users):
    shares = []
    N = len(users)
    # step 1: sort users based on beta (ascending)
    users.sort(key=lambda x: x.demand.beta, reverse=False)
    # step 2: compute the ratios
    ratios = []
    betas = []
    for user in users:
        ratio = user.demand.mem / user.demand.computation  # normalized ratio 
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
    step = 0.0001
    while (flag):
        gpumin = gpumin -1 
        if(gpumin < 0):
            print("###gpumin is negative####")
        price[0] = 1
        price[1] = betas[gpumin]
        price[2] = 1 + betas[gpumin]
        useralloc = userallocRes(betas, ratios, price)
        currLoad = sumResource(useralloc)

        if (currLoad.MilliCPU > currLoad.NvidiaGPU):
            userAllocG = userallocGPU(betas, ratios, price)
            currLoadG = sumResource(userAllocG)
            if (currLoadG.MilliCPU > currLoadG.NvidiaGPU):
                continue
            else :
                finalAlloc = useralloc
                finalAlloc[gpumin].MilliCPU = 0
                finalAlloc[gpumin].NvidiaGPU = 0
                currLoadG = sumResource(finalAlloc)
                finalAlloc[gpumin].NvidiaGPU = (currLoadG.MilliCPU - currLoadG.NvidiaGPU + (finalAlloc[gpumin].Memory/ ratios[gpumin])) / (1 + betas[gpumin])
                finalAlloc[gpumin].MilliCPU = currLoadG.NvidiaGPU + finalAlloc[gpumin].NvidiaGPU - currLoadG.MilliCPU
                break
        else:
            
            # for k = betas[gpumin + 1]; k >= betas[gpumin]; k = k - step :
            k = betas[gpumin + 1]
            while k >= betas[gpumin]:
                price[0] = 1
                price[1] = k
                price[2] = k + 1
                useralloc = userallocGPU(betas, ratios, price)
                currLoad = sumResource(useralloc)
                if (abs(currLoad.MilliCPU - currLoad.NvidiaGPU) < error) :
                    finalAlloc = useralloc
                    flag = False
                    break
                k = k - step


    if (N > 1) :
        sumAlloc = sumResource(finalAlloc)
        budget = max(sumAlloc.MilliCPU, sumAlloc.NvidiaGPU, sumAlloc.Memory) 
        for i in range(3):
            price[i] = price[i]* budget 
        for j in range(N): 
            finalAlloc[j].MilliCPU = finalAlloc[j].MilliCPU /budget
            finalAlloc[j].NvidiaGPU = finalAlloc[j].NvidiaGPU /budget
            finalAlloc[j].Memory = finalAlloc[j].Memory /budget

    # step 5: create the real shares.
    for i in range(N):
        cpu = finalAlloc[i].MilliCPU * capacity.MilliCPU
        gpu = finalAlloc[i].NvidiaGPU * capacity.NvidiaGPU
        mem = finalAlloc[i].Memory * capacity.Memory
        shares.append(Resource(int(cpu), int(mem), round(gpu)))
        # print(finalAlloc[i].toString())
    return shares


def userallocGPU(betas, ratios, currentPrices):
    userAlloc = [] 

    for j in range(len(betas)):
        beta = betas[j]
        ratio = ratios[j]
        alloc = Resource(0, 0, 0)
        alloc.Memory = min(1 / currentPrices[2], max(ratio, beta * ratio/currentPrices[1]))
        if (beta < currentPrices[1]) :
            alloc.MilliCPU = alloc.Memory/ ratio
            alloc.NvidiaGPU = 0
        else: # if beta = price, put it in GPU.
            alloc.MilliCPU = 0
            alloc.NvidiaGPU = alloc.Memory/(ratio*beta)
        userAlloc.append(alloc)

    return userAlloc 

def userallocRes(betas, ratios, currentPrices):
    userAlloc = [] 

    for j in range(len(betas)):
        beta = betas[j]
        ratio = ratios[j]
        alloc = Resource(0, 0, 0)
        alloc.Memory = min(1 / currentPrices[2], max(ratio, beta * ratio/currentPrices[1]))

        if (beta <= currentPrices[1]) :
            alloc.MilliCPU = alloc.Memory/ ratio
            alloc.NvidiaGPU = 0
        else: # if beta = price, put it in GPU.
            alloc.MilliCPU = 0
            alloc.NvidiaGPU = alloc.Memory/(ratio*beta)
        userAlloc.append(alloc)

    return userAlloc   