class Resource:
    def __init__(self, MilliCPU, Memory, NvidiaGPU):
        self.MilliCPU = MilliCPU
        self.Memory = Memory
        self.NvidiaGPU = NvidiaGPU

    def toString(self):
        strRes = "{"+str(self.MilliCPU) +","+str(self.Memory) +","+str(self.NvidiaGPU) +"}"
        return strRes
        
    def isFit(self, capacity, isGPU):
        if ((not isGPU) and (self.MilliCPU > capacity.MilliCPU)):
            return False

        if(self.Memory > capacity.Memory):
            return False

        if(isGPU and (self.NvidiaGPU > capacity.NvidiaGPU)):
            return False

        return True


def substract(aRes, bRes):
    result = Resource(0, 0, 0)
    result.MilliCPU = aRes.MilliCPU -bRes.MilliCPU
    result.Memory = aRes.Memory - bRes.Memory
    result.NvidiaGPU = aRes.NvidiaGPU -bRes.NvidiaGPU
    return result


def isFit(demand, capacity):
    if(demand.MilliCPU > capacity.MilliCPU):
        return False

    if(demand.Memory > capacity.Memory):
        return False

    if(demand.NvidiaGPU > capacity.NvidiaGPU):
        return False

    return True