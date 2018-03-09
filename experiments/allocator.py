from resource import *
from user import *

def DRF(capacity, isFDRF, users):
    # foreach user 
    resDemands = []
    shares = [0, 0, 0]
    for user in users:
    # convert to DRF or FDRF demands
        resDemand = Resource(0, 0, 0)
        if ~isFDRF:
            if user.demand.beta > 1:
                resDemand.MilliCPU = 0
                resDemand.NvidiaGPU = user.demand.computation / user.demand.beta
                resDemand.mem = user.demand.mem                
            else:
                resDemand.MilliCPU = user.demand.computation
                resDemand.NvidiaGPU = 0
                resDemand.mem = user.demand.mem                 
        else:
            resDemand.MilliCPU = user.demand.computation  / (1 + user.demand.beta)
            resDemand.NvidiaGPU = user.demand.computation / (1 + user.demand.beta)
            resDemand.mem = user.demand.mem                
                
    # compute its dorminant rates

    # compute the share for each users

    # compute normalized demand

    