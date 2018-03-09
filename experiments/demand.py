class Demand:
    def __init__ (self, computation, mem, beta):
        self.computation = computation
        self.mem = mem
        self.beta = beta

    def toString(self):
        strDemand = "(com, mem, beta) = "
        strDemand = strDemand +"("+ str(self.computation) + "," + str(self.mem) + ","+ str(self.beta) + ")"
        return strDemand