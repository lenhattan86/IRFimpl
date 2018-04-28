class Demand:
    def __init__ (self, computation, mem, beta, gpu):
        self.computation = computation
        self.mem = mem
        self.beta = beta
        self.gpu = gpu

    def toString(self):
        strDemand = "(com, mem, beta) = "
        strDemand = strDemand +"("+ str(self.computation) + "," + str(self.mem) + ","+ str(self.beta) + ")"
        return strDemand