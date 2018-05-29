IS_GOOLE = true

rows = read.csv("/ssd/projects/IRFimpl/demchange/google_3600.csv")
data = rows[,3] # cpu cores requested
## test with changepoint
library("changepoint")
set.seed(10)
m.data <- as.ts(data)
# ts.plot(m.data, xlab = "hours")

## CUSUM
# m.cusum=cpt.mean(m.data,penalty="Manual",pen.value=0.01,method="AMOC",test.stat="CUSUM")
# plot(m.cusum, type = "l", cpt.col = "blue", xlab = "Index", cpt.width = 4)
# cpts(m.cusum)

## PELT
# m.pelt=cpt.mean(m.data,method="PELT")
# plot(m.pelt, type = "l", cpt.col = "blue", xlab = "Index", cpt.width = 4)
# cpts(m.pelt)

## BinSeg ==> best for Google trace
m.binseg=cpt.mean(m.data,method="BinSeg")
plot(m.binseg, type = "l", cpt.col = "blue", xlab = "Index", cpt.width = 4)
cpts(m.binseg)

## SegNeigh
m.segneigh=cpt.mean(m.data,penalty="Asymptotic",pen.value=0.8,method="SegNeigh",Q=5,class=FALSE)
plot(m.segneigh, type = "l", cpt.col = "blue", xlab = "Index", cpt.width = 4)
# cpts(m.segneigh)

## 
