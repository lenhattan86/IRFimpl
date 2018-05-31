## ONLINE;

#generate a sequence containing two change points
# m.data <- c(rnorm(200,0,1),rnorm(200,1,1),rnorm(200,0,1))
rows = read.csv("/ssd/projects/IRFimpl/demchange/google_3600.csv")
data = rows[,3] # cpu cores requested
m.data <- as.ts(data)
#vectors to hold the result
detectiontimes <- numeric()
changepoints <- numeric()
#use a Lepage CPM
# cpm <- makeChangePointModel(cpmType="Lepage", ARL0=500)
# cpm <- makeChangePointModel(cpmType="Student", ARL0=500)
cpm <- makeChangePointModel(cpmType="normal", ARL0=500)
i <- 0
DETECTION_VALUE = i
DETECTION_VALUES = numeric()
CHANGE_POINT = m.data[i]
CHANGE_POINTS = numeric()
while (i < length(m.data)) {
    i <- i + 1
    #process each observation in turn
    cpm <- processObservation(cpm,m.data[i])
    #if a change has been found, log it, and reset the CPM
    if (changeDetected(cpm) == TRUE) {
        print(sprintf("Change detected at observation %d", i))
        detectiontimes <- c(detectiontimes,i)
        DETECTION_VALUE = m.data[i]
        #the change point estimate is the maximum D_kt statistic
        Ds <- getStatistics(cpm)
        tau <- which.max(Ds)
        if (length(changepoints) > 0) {
            tau <- tau + changepoints[length(changepoints)]
            
        }
        changepoints <- c(changepoints,tau)
        CHANGE_POINT = m.data[tau]
        #reset the CPM
        cpm <- cpmReset(cpm)
        #resume monitoring from the observation following the
        #change point
        # i <- tau
    }
    DETECTION_VALUES <- c(DETECTION_VALUES,DETECTION_VALUE)
    CHANGE_POINTS <- c(CHANGE_POINTS,CHANGE_POINT)
}

ts.plot(m.data, xlab = "hours", ylab = "cpu cores",  ylim = c(0, 8000))
# lines(DETECTION_VALUES,col="blue")
abline(v=detectiontimes, col="blue")
lines(CHANGE_POINTS,col="green")
legend(1, 1000, legend=c("demand", "detection", "change points"),
       col=c("black", "blue", "green"), lty=1:2, cex=0.8)
