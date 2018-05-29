# https://rdrr.io/cran/onlineCPD/man/onlineCPD.html

### THIS package was REMOVED from CRAN

# install.packages("onlineCPD")
library(onlineCPD)

##### Univariate Data #####
set.seed(6)
x <- c(rnorm(50,mean=0.3,sd=0.15),rnorm(40,mean=0.7,sd=0.1),rnorm(60,mean=0.5,sd=0.15))
res <- onlineCPD(datapt=x[1])
for(k in x)
  res <- onlineCPD(res,k)
plot(res)

##### Real Multivariate Data #####
data(WalBelSentiment)
data(WalBelTimes)
res <- onlineCPD(datapt=WalBelSentiment[1400,],timept=WalBelTimes[1400])
for(k in 1401:1600)
  res <- onlineCPD(res,WalBelSentiment[k,],WalBelTimes[k])
plot(res)

## You can use onlineCPD to add points to an existing "oCPD" object
y <- c(rnorm(50,0.5,0.1),rnorm(20,0.48,0.02),rnorm(50,0.5,0.1))
res <- offlineCPD(y)
plot(res)
x <- rnorm(75,0.7,0.4)
for(k in x)
  res <- onlineCPD(res,k)
plot(res)