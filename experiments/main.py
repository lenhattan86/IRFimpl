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

NUM_NODES = 2
NUM_PHY_CPU_PER_NODE = 2
NUM_CORES_PER_CPU = 22 # max cpu - 1 - num(gpus a node)/cpus
NUM_PHY_GPU_PER_NODE = 2
MEM_PER_NODE = 120 * Gi #134956859392 bytes

CPU_OVERHEADS = 0
MEM_OVERHEADS = 0


       
def createDRFExperiement():
    print('DRF experiemnts')
    ## for DRF134956859392
    f = open(this_path +'/' + 'DRF_experiments.sh','w')
    f.write('dummy file')
    f.close()

def computeDemand(jobs, capacity):
    demand = Demand(0, 0, 0)
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

def main():
    
    # capacity = Resource(48000, 128*1024*1024, 4)
    CPU = NUM_NODES* NUM_PHY_CPU_PER_NODE * NUM_CORES_PER_CPU
    GPU = NUM_NODES* NUM_PHY_GPU_PER_NODE
    MEM = MEM_PER_NODE * NUM_NODES
    # capacity = Resource(10000, 128, 12)
    capacity = Resource(CPU*1000, MEM, GPU)
    # scheduler='kube-scheduler'
    scheduler='my-scheduler'
    isQueuedUp = True
    isBestFit = False # MUST BE False


    userStrArray = ["user1", "user2"]
    userJobNums = [60, 3000]
    users = []

    workload = 'traces/motivation'
    # workload = 'traces/simple1.1'
    startLogTime = 0
    stopTime = 4000
    extraTime = 30*60 # 30 minutes
    monitor_time = int(stopTime + extraTime)
    interval = 1

    for strUser in userStrArray:
        # print("read " + strUser)
        jobs = readJobs(this_path+"/"+workload, strUser+".txt")        
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
        jobs = user.jobs[1:userJobNums[i]]
        loggedJobs = toActiveJobs(jobs) 
        print("Prepare the jobs for " + user.username + ": " + str(userJobNums[i])) 
        prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp)  
    return

    print("====================== ES ALLOCATION =====================")
    expFolder = "ES"
    shares = ES(capacity, users)   
    printShares(shares) 
    # given fill the jobs & allocation enforce,  prepare the job cripts
    mainShell(users, expFolder, monitor_time, interval, startLogTime)
    for i in range(len(users)):
    # for i in range(1):
        user = users[i]
        share = shares[i]
        jobs = user.jobs[:]
        loggedJobs = enforceAllocation(share, jobs, stopTime, isBestFit) 
        if isBestFit:
            print("Prepare the jobs for " + user.username + ": " + str(len(loggedJobs)))  
            prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp)        

    print("====================== DRF ALLOCATION =====================")
    expFolder = "DRF"
    shares = DRF(capacity, False, users)   
    printShares(shares) 
    # given fill the jobs & allocation enforce,  prepare the job cripts
    mainShell(users, expFolder, monitor_time, interval, startLogTime)
    for i in range(len(users)):
    # for i in range(1):
        user = users[i]
        share = shares[i]
        jobs = user.jobs[:]
        loggedJobs = enforceAllocation(share, jobs, stopTime, isBestFit) 
        if isBestFit:
            print("Prepare the jobs for " + user.username + ": " + str(len(loggedJobs)))  
            prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp)    

    print("====================== Naive DRF ALLOCATION =====================")
    expFolder = "naiveDRF"
    demands=[]
    demands.append(Resource(1000,12*GI, 1))
    demands.append(Resource(1000,12*GI, 1))
    shares = naiveDRF(capacity, False, users, demands)   
    printShares(shares) 
    # given fill the jobs & allocation enforce,  prepare the job cripts
    mainShell(users, expFolder, monitor_time, interval, startLogTime)
    for i in range(len(users)):
    # for i in range(1):
        user = users[i]
        share = shares[i]
        jobs = user.jobs[:]
        loggedJobs = enforceAllocation(share, jobs, stopTime, isBestFit) 
        if isBestFit:
            print("Prepare the jobs for " + user.username + ": " + str(len(loggedJobs)))  
            prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp)    

    print("====================== Static ALLOCATION =====================")
    expFolder = "static"
    shares = Static(capacity, users)   
    printShares(shares) 
    # given fill the jobs & allocation enforce,  prepare the job cripts
    mainShell(users, expFolder, monitor_time, interval, startLogTime)
    for i in range(len(users)):
    # for i in range(1):
        user = users[i]
        share = shares[i]
        jobs = user.jobs[:]
        loggedJobs = enforceAllocation(share, jobs, stopTime, isBestFit) 
        if isBestFit:
            print("Prepare the jobs for " + user.username + ": " + str(len(loggedJobs)))  
            prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp)    

    print("====================== Static2 ALLOCATION =====================")
    expFolder = "static2"
    shares = Static2(capacity, users)   
    printShares(shares) 
    # given fill the jobs & allocation enforce,  prepare the job cripts
    mainShell(users, expFolder, monitor_time, interval, startLogTime)
    for i in range(len(users)):
    # for i in range(1):
        user = users[i]
        share = shares[i]
        jobs = user.jobs[:]
        loggedJobs = enforceAllocation(share, jobs, stopTime, isBestFit) 
        if isBestFit:
            print("Prepare the jobs for " + user.username + ": " + str(len(loggedJobs)))  
            prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp)             

    print("====================== FDRF ALLOCATION =====================")
    expFolder = "FDRF"
    shares = DRF(capacity, True, users)   
    printShares(shares) 
    # given fill the jobs & allocation enforce,  prepare the job cripts
    mainShell(users, expFolder, monitor_time, interval, startLogTime)
    for i in range(len(users)):
    # for i in range(1):
        user = users[i]
        share = shares[i]
        jobs = user.jobs[:]
        loggedJobs = enforceAllocation(share, jobs, stopTime, isBestFit) 
        if isBestFit:
            print("Prepare the jobs for " + user.username + ": " + str(len(loggedJobs)))  
            prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp)    


    print("====================== Pricing ALLOCATION =====================")
    expFolder = "Pricing"
    shares = Pricing(capacity, True, users)
    printShares(shares) 
    # given fill the jobs & allocation enforce,  prepare the job cripts
    mainShell(users, expFolder, monitor_time, interval, startLogTime)
    for i in range(len(users)):
    # for i in range(1):
        user = users[i]
        share = shares[i]
        jobs = user.jobs[:]
        loggedJobs = enforceAllocation(share, jobs, stopTime, isBestFit) 
        if isBestFit:
            print("Prepare the jobs for " + user.username + ": " + str(len(loggedJobs)))  
            prepareKubernetesJobs(user.username, scheduler, expFolder, loggedJobs, isQueuedUp)    


    print("==================================================================")
    print("capacity: "+capacity.toString())
    print("isBestFit: "+str(isBestFit) )   
    print("isQueuedUp: "+str(isQueuedUp) ) 
    print("scheduler: "+str(scheduler) ) 
    print("==================================================================")

if __name__ == "__main__": main()