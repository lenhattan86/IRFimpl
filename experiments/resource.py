Gi = 1024*1024*1024

class Resource:
    def __init__(self, MilliCPU, Memory, NvidiaGPU):
        self.MilliCPU = MilliCPU
        self.Memory = Memory
        self.NvidiaGPU = NvidiaGPU

    def createNorm(self, baseRes):
        self.norm = Resource(self.MilliCPU/ baseRes.MilliCPU, self.Memory / baseRes.Memory, self.NvidiaGPU / baseRes.NvidiaGPU)
        self.baseRes = baseRes

    def toString(self):
        strRes = "{"+str(self.MilliCPU) +" MilliCPU,"+str(self.Memory/Gi) +" Gi,"+str(self.NvidiaGPU) +" gpus}"
        # strRes = "{"+str(self.MilliCPU) +" MilliCPU,"+str(self.Memory) +" bytes,"+str(self.NvidiaGPU) +" gpus}"
        return strRes
        
    def isFit(self, capacity, isGPU):
        if ((not isGPU) and (self.MilliCPU > capacity.MilliCPU)):
            return False

        if(self.Memory > capacity.Memory):
            return False

        if(isGPU and (self.NvidiaGPU > capacity.NvidiaGPU)):
            return False

        return True

def sumResource(resources):
    result = Resource(0,0,0)
    for res in resources:
        result.MilliCPU = result.MilliCPU + res.MilliCPU
        result.Memory = result.Memory + res.Memory
        result.NvidiaGPU = result.NvidiaGPU + res.NvidiaGPU

    return result

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