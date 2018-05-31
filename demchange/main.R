IS_GOOLE = true

rows = read.csv("/ssd/projects/IRFimpl/demchange/google_3600.csv")
data = rows[,3] # cpu cores requested
## test with changepoint
library("changepoint")
set.seed(10)
m.data <- as.ts(data)
ts.plot(m.data, xlab = "hours", ylab = "cpu cores",  ylim = c(0, 8000))

# BinSeg ==> best for Google trace
# m.binseg=cpt.mean(m.data, method="BinSeg", Q=15)
# plot(m.binseg, type = "l", cpt.col = "blue", , xlab = "hours", ylab = "cpu cores",  ylim = c(0, 8000), cpt.width = 4)
# cpts(m.binseg)

# same without CUSUM.
# m.binseg=cpt.mean(m.data, method="BinSeg", Q=10)
# plot(m.binseg, type = "l", cpt.col = "blue", , xlab = "hours", ylab = "cpu cores",  ylim = c(0, 8000), cpt.width = 4)
# cpts(m.binseg)


#2. PELT
# 100000 * log(n)
m.pelt=cpt.mean(m.data, method="PELT")
m.pelt=cpt.mean(m.data, penalty="Manual", pen.value = "100000 * log(n)", method="PELT")
# m.pelt=cpt.mean(m.data, penalty='Asymptotic', pen.value=0.99, method="PELT")
plot(m.pelt, type = "l", cpt.col = "blue", xlab = "hours", ylab = "cpu cores",  ylim = c(0, 8000), cpt.width = 4)
cpts(m.pelt)


#sumary:
# cpt.mean: test.stat = "Normal" or "CUSUM"
# cpt.var: test.stat  = "Normal" or "CSS"
# cpt.meanvar: test.stat = "Gamma", "Normal", "Poisson", "Exponential"

# penalty type: SIC (log(n)), BIC, Manual (constant of function in text) ** n: number of data points.


