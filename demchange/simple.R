# install.packages("changepoint")
library("changepoint")
set.seed(10)
m.data <- c(rnorm(100, 0, 1), rnorm(100, 1, 1), rnorm(100, 0, 1), rnorm(100, 0.2, 1))
ts.plot(m.data, xlab = "Index")

m.pelt <- cpt.mean(m.data, method = "PELT")
plot(m.pelt, type = "l", cpt.col = "blue", xlab = "Index", cpt.width = 4)
cpts(m.pelt)

# m.binseg <- cpt.mean(m.data, method = "BinSeg")
# plot(m.binseg, type = "l", xlab = "Index", cpt.width = 4)
# cpts(m.binseg)