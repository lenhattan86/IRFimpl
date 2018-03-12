import os 
import allocator
from job import *
from user import *
from demand import *
from resource import *
from allocator import *
from kubernetes import *

this_path = os.path.dirname(os.path.realpath(__file__))
NUM_NODES = 2
NUM_PHY_CPU_PER_NODE = 2
NUM_CORES_PER_CPU = 24
NUM_PHY_GPU_PER_NODE = 2
MEM_PER_NODE = 128 # Gi

CPU_OVERHEADS = 0
MEM_OVERHEADS = 0
       
def createDRFExperiement():
    print('DRF experiemnts')
     ## for DRF
    f = open(this_path +'/' + 'DRF_experiments.sh','w')
    f.write('dummy file')
    f.close()

def computeDemand(jobs):
    demand = Demand(0, 0, 0)
    cpuTime = 0.0
    gpuTime = 0.0    
    for job in jobs:        
        cpuTime = cpuTime + job.cpuProfile.compl
        gpuTime = gpuTime + job.gpuProfile.compl
        demand.computation = demand.computation + job.cpuProfile.demand.MilliCPU *  job.cpuProfile.compl
        demand.mem = demand.mem + job.cpuProfile.demand.Memory *  job.cpuProfile.compl

    demand.beta = cpuTime / gpuTime
    demand.computation = demand.computation/ cpuTime
    demand.mem = demand.mem/ cpuTime
    return demand

def printShares(shares):
    strShares = "{"
    for share in shares:
        strShares = strShares + share.toString() + ","
    strShares = strShares + "}"
    print(strShares)

def main():
    # capacity = Resource(48000, 128*1024*1024, 4)
    CPU = NUM_NODES* NUM_PHY_CPU_PER_NODE * NUM_CORES_PER_CPU
    GPU = NUM_NODES* NUM_PHY_GPU_PER_NODE
    MEM = MEM_PER_NODE * NUM_NODES
    # capacity = Resource(10000, 128, 12)    
    capacity = Resource(CPU*1000, MEM, GPU)
    print("capacity: "+capacity.toString())    

    userStrArray = ["user1", "user2", "user3"]
    users = []
    workload = 'simple'
    for strUser in userStrArray:
        # print("read " + strUser)
        jobs = readJobs(this_path+"/"+workload, strUser+".txt")        
        # compute betas
        demand = computeDemand(jobs)
        print(demand.toString())
        newUser = User(strUser, demand, jobs)
        # print(newUser.toString())
        users.append(newUser)
    # allocators
    print("====================== ALLOCATION =====================")
    shares = DRF(capacity, False, users)   
    printShares(shares) 

    # given fill the jobs & allocation enforce,  prepare the job cripts
    print("================= Resource Enforcement ================")
    for i in range(len(users)):
    # for i in range(1):
        print("Prepare the jobs for " + users[i].username)
        loggedJobs = enforceAllocation(shares[i], users[i].jobs)   
        prepareKubernetesJobs(users[i].username, loggedJobs)

    mainShell(users)

if __name__ == "__main__": main()