import os 
import allocator
from job import *
from user import *
from demand import *
from resource import *
from allocator import *
from kubernetes import *

this_path = os.path.dirname(os.path.realpath(__file__))
Gi = 1024*1024*1024
MILLI=1000

      
def createDRFExperiement():
    print('DRF experiemnts')
    ## for DRF134956859392
    f = open(this_path +'/' + 'DRF_experiments.sh','w')
    f.write('dummy file')
    f.close()

def computeDemand_bk(jobs, capacity):
    demand = Demand(0, 0, 0, 0)
    cpuTime = 0.0
    gpuTime = 0.0    
    gpuDemand = 0.0
    for job in jobs:        
        cpuTime = cpuTime + job.cpuProfile.compl
        gpuTime = gpuTime + job.gpuProfile.compl
        demand.computation = (demand.computation + job.cpuProfile.demand.MilliCPU *  job.cpuProfile.compl) 
        gpuDemand = gpuDemand + job.gpuProfile.demand.NvidiaGPU *  job.gpuProfile.compl 
        demand.mem = demand.mem + job.cpuProfile.demand.Memory *  job.cpuProfile.compl

    # normalize demands
    demand.computation = demand.computation / capacity.MilliCPU
    gpuDemand = gpuDemand / capacity.NvidiaGPU
    demand.beta = demand.computation / gpuDemand 

    demand.mem = demand.mem / capacity.Memory / cpuTime
    demand.computation = demand.computation / cpuTime

    return demand

def computeDemandOld(jobs, capacity):
    demand = Demand(0, 0, 0, 0)    
    job = jobs[0]
    absoluteBeta = job.cpuProfile.demand.MilliCPU / job.gpuProfile.demand.NvidiaGPU * job.cpuProfile.compl / job.gpuProfile.compl
    demand.computation = absoluteBeta
    demand.beta = absoluteBeta*capacity.NvidiaGPU/capacity.MilliCPU
    demand.mem = job.cpuProfile.demand.Memory*capacity.MilliCPU/capacity.Memory
    return demand


def computeDemand(jobs, capacity):
    demand = Demand(0, 0, 0, 0, 0)    
    job = jobs[0]
    absoluteBeta = job.cpuProfile.compl / job.gpuProfile.compl
    demand.computation = job.cpuProfile.demand.MilliCPU
    # demand.beta = absoluteBeta * job.cpuProfile.demand.MilliCPU / job.gpuProfile.demand.NvidiaGPU  * capacity.NvidiaGPU / capacity.MilliCPU
    demand.beta = absoluteBeta * job.cpuProfile.demand.MilliCPU / job.gpuProfile.demand.NvidiaGPU
    demand.mem  = job.cpuProfile.demand.Memory
    demand.gpu  = job.gpuProfile.demand.NvidiaGPU
    demand.gpu_mem  = job.gpuProfile.demand.Memory

    return demand

def main():
    
    scheduler='my-scheduler'
    isQueuedUp = True
    isBestFit = False # MUST BE False

    startLogTime = 0
    stopTime = 3000
    # extraTime = 30*60 # 30 minutes
    extraTime = 0 # 30 minutes
    monitor_time = int(stopTime + extraTime)
    interval = 5

    isOfficial = True
    if isOfficial:
        # capacity = Resource(384*1000, 1152*GI, 12)
        capacity = Resource(384*1000, 1152*GI, 12)
        workload = 'traces/evaluation'
        # userStrArray = ["user1", "user2", "user3", "user4"]
        # jobRepNums = [2000, 2000, 2000, 2000]
        # userJobNums = [600, 600, 600, 600]
        # userJobNums = [24, 24, 24, 24]
        userStrArray = ["user1", "user2", "user3"]
        jobRepNums = [1000, 1000, 1000]
        userJobNums = [200, 200, 200]        
        traditionalDemands=[]
        traditionalDemands.append(Resource(1000,3*GI, 1))
        traditionalDemands.append(Resource(1000,3*GI, 1))
        traditionalDemands.append(Resource(1000,3*GI, 1))
    else:        
        # workload = 'traces/motivation'
        capacity = Resource(88*1000, 240*GI, 4)
        workload = 'traces/real1.0'
        userStrArray = ["user1", "user2"]
        jobRepNums = [2000, 2000]
        userJobNums = [60, 3000]
        traditionalDemands=[]
        traditionalDemands.append(Resource(1000,12*GI, 1))
        traditionalDemands.append(Resource(1000,12*GI, 1))
        
    users = []
    
    for i in range(len(userStrArray)):
        strUser=userStrArray[i]
        # print("read " + strUser)
        jobs = readJobs(this_path+"/"+workload, strUser+".txt", jobRepNums[i])        
        # compute betas
        demand = computeDemand(jobs, capacity)
        print(demand.toString())
        newUser = User(strUser, demand, jobs)
        # print(newUser.toString())
        users.append(newUser)    

    print("================ prepare jobs for all Allocations =======")  
    expFolder="exp"      
    mainShell(users, expFolder, monitor_time, interval, startLogTime)
    for i in range(len(users)):
    # for i in range(1):
        user = users[i]
        jobs = user.jobs[0:userJobNums[i]]
        loggedJobs = toActiveJobs(jobs) 
        #print("Prepare the jobs for " + user.username + ": " + str(userJobNums[i])) 
        prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp)  
    
    # return

    # print("====================== ES ALLOCATION =====================")
    # expFolder = "ES"
    # shares = ES(capacity, users)   
    # printShares(shares) 
    # # given fill the jobs & allocation enforce,  prepare the job cripts
    # mainShell(users, expFolder, monitor_time, interval, startLogTime)
    # for i in range(len(users)):
    # # for i in range(1):
    #     user = users[i]
    #     share = shares[i]
    #     jobs = user.jobs[:]
    #     loggedJobs = enforceAllocation(share, jobs, stopTime, isBestFit) 
    #     print("Number of admitted jobs for " + user.username + ": " + str(len(loggedJobs)))  
    #     if isBestFit:
    #         prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp) 
    #     else:
    #         jobs = user.jobs[0:userJobNums[i]]
    #         loggedJobs = toActiveJobs(jobs) 
    #         #print("Prepare the jobs for " + user.username + ": " + str(userJobNums[i])) 
    #         prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp)         

    
    # print("====================== Naive DRF ALLOCATION =====================")
    # expFolder = "naiveDRF"    
    # shares = naiveDRF(capacity, False, users, traditionalDemands)   
    # printShares(shares) 
    # # given fill the jobs & allocation enforce,  prepare the job cripts
    # mainShell(users, expFolder, monitor_time, interval, startLogTime)
    # for i in range(len(users)):
    # # for i in range(1):
    #     user = users[i]
    #     share = shares[i]
    #     jobs = user.jobs[:]
    #     loggedJobs = enforceAllocation(share, jobs, stopTime, isBestFit) 
    #     print("Number of admitted jobs for " + user.username + ": " + str(len(loggedJobs)))  
    #     if isBestFit: 
    #         prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp)
    #     else:
    #         jobs = user.jobs[0:userJobNums[i]]
    #         loggedJobs = toActiveJobs(jobs) 
    #         #print("Prepare the jobs for " + user.username + ": " + str(userJobNums[i])) 
    #         prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp)       

    # if not isOfficial:
    #     print("====================== Static ALLOCATION =====================")
    #     expFolder = "static"
    #     shares = Static(capacity, users)   
    #     printShares(shares) 
    #     # given fill the jobs & allocation enforce,  prepare the job cripts
    #     mainShell(users, expFolder, monitor_time, interval, startLogTime)
    #     for i in range(len(users)):
    #     # for i in range(1):
    #         user = users[i]
    #         share = shares[i]
    #         jobs = user.jobs[:]
    #         loggedJobs = enforceAllocation(share, jobs, stopTime, isBestFit) 
    #         print("Number of admitted jobs for " + user.username + ": " + str(len(loggedJobs)))  
    #         if isBestFit:
    #             prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp) 
    #         else:
    #             jobs = user.jobs[0:userJobNums[i]]
    #             loggedJobs = toActiveJobs(jobs) 
    #             #print("Prepare the jobs for " + user.username + ": " + str(userJobNums[i])) 
    #             prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp)      

    #     print("====================== Static2 ALLOCATION =====================")
    #     expFolder = "static2"
    #     shares = Static2(capacity, users)   
    #     printShares(shares) 
    #     # given fill the jobs & allocation enforce,  prepare the job cripts
    #     mainShell(users, expFolder, monitor_time, interval, startLogTime)
    #     for i in range(len(users)):
    #     # for i in range(1):
    #         user = users[i]
    #         share = shares[i]
    #         jobs = user.jobs[:]
    #         loggedJobs = enforceAllocation(share, jobs, stopTime, isBestFit) 
    #         print("Number of admitted jobs for " + user.username + ": " + str(len(loggedJobs)))  
    #         if isBestFit:
    #             prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp)
    #         else:
    #             jobs = user.jobs[0:userJobNums[i]]
    #             loggedJobs = toActiveJobs(jobs) 
    #             #print("Prepare the jobs for " + user.username + ": " + str(userJobNums[i])) 
    #             prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp)             

    print("====================== AlloX ALLOCATION =====================")
    expFolder = "allox"
    shares = allox(capacity, users)
    printShares(shares) 
    # given fill the jobs & allocation enforce,  prepare the job cripts
    # mainShell(users, expFolder, monitor_time, interval, startLogTime)
    # for i in range(len(users)):    
    #     user = users[i]
    #     share = shares[i]
    #     jobs = user.jobs[:]
    #     loggedJobs = enforceAllocation(share, jobs, stopTime, isBestFit) 
    #     print("Number of admitted jobs for " + user.username + ": " + str(len(loggedJobs)))  
    #     if isBestFit:
    #         prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp) 
    #     else:
    #         jobs = user.jobs[0:userJobNums[i]]
    #         loggedJobs = toActiveJobs(jobs) 
    #         #print("Prepare the jobs for " + user.username + ": " + str(userJobNums[i])) 
    #         prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp)      


    print("==================================================================")
    print("capacity: "+capacity.toString())
    print("isBestFit: "+str(isBestFit) )   
    print("isQueuedUp: "+str(isQueuedUp) ) 
    print("scheduler: "+str(scheduler) ) 
    print("workload: "+ workload)
    print("==================================================================")

if __name__ == "__main__": main()