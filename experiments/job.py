class Job:    
    def __init__ (self, cpuProfile, gpuProfile, beta, command):
        self.cpuProfile = cpuProfile
        self.gpuProfile = gpuProfile
        self.beta = beta
        self.command = command


class JobProfile:
    def __init__(self, cpu, gpu, mem, compl):
        self.cpu = cpu
        self.gpu = gpu
        self.mem = mem
        self.compl = compl


def readJobs(this_path, jobFile):    
    # try:
    f = open(this_path + '/' + jobFile)
    # except:
    #     print("cannot read file : " + this_path + '/' + jobFile)
    #     return []

    lines = f.readlines()
    jobs = []
    JOB_LINES = 4
    jobLineCount = 0

    for line in lines:
        strLine = line.strip()
        if not strLine.startswith("#"):            
            
            jobLineCount = jobLineCount + 1
            strArray = strLine.split()

            if (jobLineCount == 1):                
                jobId = int(strLine)

            elif(jobLineCount == 2):
                cCpu = int(strArray[0])
                cGPu = int(strArray[1]) # must be zero
                cMem = int(strArray[2])
                cCompl = int(strArray[3])                

            elif(jobLineCount == 3):
                gCpu = int(strArray[0])
                gGPu = int(strArray[1])
                gMem = int(strArray[2])
                gCompl = int(strArray[3])         
                

            elif(jobLineCount == JOB_LINES):     
                beta  = cCompl/gCompl           
                command = strLine
                cpuProfile = JobProfile(cCpu, cGPu, cMem, cCompl)
                gpuProfile = JobProfile(gCpu, gGPu, gMem, gCompl)
                job = Job(cpuProfile, gpuProfile, beta, command)
                jobs.append(job)
                
                jobLineCount = 0
                

    f.close()
    return jobs