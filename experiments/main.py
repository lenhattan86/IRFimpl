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

NUM_NODES = 2
NUM_PHY_CPU_PER_NODE = 2
NUM_CORES_PER_CPU = 23
NUM_PHY_GPU_PER_NODE = 2
MEM_PER_NODE = 120 * Gi #134956859392 bytes

CPU_OVERHEADS = 0
MEM_OVERHEADS = 0

CPU_TO_GPU_RATIO = NUM_PHY_CPU_PER_NODE*NUM_CORES_PER_CPU/NUM_PHY_GPU_PER_NODE * 1000
       
def createDRFExperiement():
    print('DRF experiemnts')
    ## for DRF134956859392
    f = open(this_path +'/' + 'DRF_experiments.sh','w')
    f.write('dummy file')
    f.close()

def computeDemand(jobs, cpu2gpuRatio):
    demand = Demand(0, 0, 0)
    cpuTime = 0.0
    gpuTime = 0.0    
    gpuDemand = 0.0
    for job in jobs:        
        cpuTime = cpuTime + job.cpuProfile.compl
        gpuTime = gpuTime + job.gpuProfile.compl
        demand.computation = demand.computation + job.cpuProfile.demand.MilliCPU *  job.cpuProfile.compl
        gpuDemand = gpuDemand + job.gpuProfile.demand.NvidiaGPU *  job.gpuProfile.compl
        demand.mem = demand.mem + job.cpuProfile.demand.Memory *  job.cpuProfile.compl

    # demand.beta = cpuTime / gpuTime
    demand.beta = demand.computation / gpuDemand / cpu2gpuRatio
    demand.computation = demand.computation/ cpuTime
    demand.mem = demand.mem/ cpuTime
    return demand

def main():
    # capacity = Resource(48000, 128*1024*1024, 4)
    CPU = NUM_NODES* NUM_PHY_CPU_PER_NODE * NUM_CORES_PER_CPU
    GPU = NUM_NODES* NUM_PHY_GPU_PER_NODE
    MEM = MEM_PER_NODE * NUM_NODES
    # capacity = Resource(10000, 128, 12)
    capacity = Resource(CPU*1000, MEM, GPU)
    print("capacity: "+capacity.toString())    

    userStrArray = ["user1", "user2"]
    users = []

    workload = 'real1.0'
    # workload = 'simple1.1'
    stopTime = 2000
    monitor_time = 2000
    interval = 1

    for strUser in userStrArray:
        # print("read " + strUser)
        jobs = readJobs(this_path+"/"+workload, strUser+".txt")        
        # compute betas
        demand = computeDemand(jobs, CPU_TO_GPU_RATIO)
        print(demand.toString())
        newUser = User(strUser, demand, jobs)
        # print(newUser.toString())
        users.append(newUser)        
        
    print("====================== ES ALLOCATION =====================")
    expFolder = "ES"
    shares = ES(capacity, users)   
    printShares(shares) 
    # given fill the jobs & allocation enforce,  prepare the job cripts
    print("================= Resource Enforcement ================")    
    mainShell(users, expFolder, monitor_time, interval)
    for i in range(len(users)):
    # for i in range(1):
        user = users[i]
        share = shares[i]
        jobs = user.jobs[:]
        loggedJobs = enforceAllocation(share, jobs, stopTime) 
        print("Prepare the jobs for " + user.username + ": " + str(len(loggedJobs)))  
        prepareKubernetesJobs(user.username, expFolder, loggedJobs)        

    print("====================== DRF ALLOCATION =====================")
    expFolder = "DRF"
    shares = DRF(capacity, False, users, CPU_TO_GPU_RATIO)   
    printShares(shares) 
    # given fill the jobs & allocation enforce,  prepare the job cripts
    print("================= Resource Enforcement ================")   
    mainShell(users, expFolder, monitor_time, interval)
    for i in range(len(users)):
    # for i in range(1):
        user = users[i]
        share = shares[i]
        jobs = user.jobs[:]
        loggedJobs = enforceAllocation(share, jobs, stopTime) 
        print("Prepare the jobs for " + user.username + ": " + str(len(loggedJobs)))  
        prepareKubernetesJobs(user.username, expFolder, loggedJobs)

    print("====================== FDRF ALLOCATION =====================")
    expFolder = "FDRF"
    shares = DRF(capacity, True, users,CPU_TO_GPU_RATIO)   
    printShares(shares) 
    # given fill the jobs & allocation enforce,  prepare the job cripts
    print("================= Resource Enforcement ================")    
    mainShell(users, expFolder, monitor_time, interval)
    for i in range(len(users)):
    # for i in range(1):
        user = users[i]
        share = shares[i]
        jobs = user.jobs[:]
        loggedJobs = enforceAllocation(share, jobs, stopTime) 
        print("Prepare the jobs for " + user.username + ": " + str(len(loggedJobs)))  
        prepareKubernetesJobs(user.username, expFolder, loggedJobs)




    print("====================== Pricing ALLOCATION =====================")
    expFolder = "Pricing"
    shares = Pricing(capacity, True, users)
    printShares(shares) 
    # given fill the jobs & allocation enforce,  prepare the job cripts
    print("================= Resource Enforcement ================")    
    mainShell(users, expFolder, monitor_time, interval)
    for i in range(len(users)):
    # for i in range(1):
        user = users[i]
        share = shares[i]
        jobs = user.jobs[:]
        loggedJobs = enforceAllocation(share, jobs, stopTime) 
        print("Prepare the jobs for " + user.username + ": " + str(len(loggedJobs)))  
        prepareKubernetesJobs(user.username, expFolder, loggedJobs)  

if __name__ == "__main__": main()