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
        # strRes = "{"+str(self.MilliCPU) +" MilliCPU, "+str(self.Memory) +" bytes, "+str(self.NvidiaGPU) +" gpus}"
        return strRes

    def normalize(self, capacity):
        normalizeRes = Resource(0,0,0)
        normalizeRes.MilliCPU = float(self.MilliCPU/capacity.MilliCPU)
        normalizeRes.Memory = float(self.Memory/capacity.Memory)
        normalizeRes.NvidiaGPU = float(self.MilliCPU/capacity.NvidiaGPU)
        return normalizeRes
        
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

def sumResourceNorm(resources, capacity):
    result = Resource(0,0,0)
    for res in resources:
        result.MilliCPU = result.MilliCPU + res.MilliCPU
        result.Memory = result.Memory + res.Memory
        result.NvidiaGPU = result.NvidiaGPU + res.NvidiaGPU

    result.MilliCPU = 1.0*result.MilliCPU/capacity.MilliCPU
    result.Memory = 1.0*result.Memory/capacity.Memory
    result.NvidiaGPU = 1.0*result.NvidiaGPU/capacity.NvidiaGPU

    return result    

def sumNormalizedLoads(betas, resources):
    result = Resource(0,0,0)
    for i in range(len(resources)):
    # for res in resources:
        beta = betas[i]
        res = resources[i]
        result.MilliCPU = result.MilliCPU + res.MilliCPU
        result.Memory = result.Memory + res.Memory
        result.NvidiaGPU = result.NvidiaGPU + res.NvidiaGPU*beta

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