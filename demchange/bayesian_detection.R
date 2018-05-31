source("https://raw.githubusercontent.com/chenhaotian/Changepoints/master/online_detection/bayesian.r")


################################################### Examples ######################################################

## Generate random samples with real changepoints: 100,170,240,310,380 
m.data <- c(rnorm(100,sd=0.5),rnorm(70,mean=5,sd=0.5),rnorm(70,mean = 2,sd=0.5),rnorm(70,sd=0.5),rnorm(70,mean = 7,sd=0.5)) 

# rows = read.csv("/ssd/projects/IRFimpl/demchange/google_3600.csv")
# data = rows[,3] # cpu cores requested
# m.data <- as.ts(data)

## online changepoint detection for series X 
m.bayesian <- onlinechangepoint(m.data, 
                          model = "nng", #"nng", "bb", "pg",
                          mu0=0.7,k0=1,alpha0=1/2,beta0=1, #initial parameters 
                          bpmethod = "mean", 
                          lambda=50, #exponential hazard 
                          FILTER=1e-3) 
tmpplot(m.bayesian,m.data) # visualize original data and run length distribution 