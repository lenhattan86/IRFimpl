class Demand:
    def __init__ (self, computation, mem, beta, gpu, gpu_mem):
        self.computation = computation
        self.mem = mem
        self.beta = beta
        self.gpu = gpu
        self.gpu_mem = gpu_mem

    def toString(self):
        strDemand = "(com, mem, beta) = "
        strDemand = strDemand +"("+ str(self.computation) + "," + str(self.mem) + ","+ str(self.beta) + ")"
        return strDemand