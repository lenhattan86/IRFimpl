import os 
import allocator
from job import *
from user import *
from demand import *
from resource import *



this_path = os.path.dirname(os.path.realpath(__file__))
       
def createDRFExperiement():
    print('DRF experiemnts')
     ## for DRF
    f = open(this_path +'/' + 'DRF_experiments.sh','w')
    f.write('dummy file')
    f.close()

def computeDemand(jobs):
    demand = Demand(0, 0, -1.0)
    avgBeta = 0.0
    totalTime = 0.0
    for job in jobs:
        avgBeta = avgBeta + job.beta
        demand.computation = demand.computation + job.cpuProfile.cpu *  job.cpuProfile.compl
        demand.mem = demand.mem + job.cpuProfile.mem *  job.cpuProfile.compl
        totalTime = totalTime + job.cpuProfile.compl

    demand.beta = avgBeta / totalTime
    demand.computation = demand.computation/ totalTime
    demand.mem = demand.mem/ totalTime
    return demand

def main():
    capacity = Resource(48000, 128*1024*1024, 4)
    betas = [2, 1, 0.5]
    userStrArray = ["user1", "user2"]
    users = []
    for strUser in userStrArray:
        print("read " + strUser)
        jobs = readJobs(this_path, strUser+".txt")        
        #   compute betas
        demand = computeDemand(jobs)        
        newUser = User(strUser, demand, jobs)
        print(newUser.toString())
        users.append(newUser)
    
    print("Experiments for IRA")
    createDRFExperiement()   

    ## for FDRF

if __name__ == "__main__": main()