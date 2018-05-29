# ecp: An R Package for Nonparametric Multiple Change Point Analysis of Multivariate Data
# Hierarchical estimation can be based upon either a divisive or agglomerative algorithm. Divisive estimation
# sequentially identifies change points via a bisection algorithm. The agglomerative algorithm
# estimates change point locations by determining an optimal segmentation.
# This provides an advantage over many existing change point algorithms which are only able to detect changes within the marginal distributions
# install.packages("ecp")
set.seed(250)
library("ecp")
period1 <- rnorm(100)
period2 <- rnorm(100, 0, 3)
period3 <- rnorm(100, 2, 1)
period4 <- rnorm(100, 2, 4)
Xnorm <- matrix(c(period1, period2, period3, period4), ncol = 1)
output1 <- e.divisive(Xnorm, R = 499, alpha = 1)
output2 <- e.divisive(Xnorm, R = 499, alpha = 2)
output2$estimates

output1$k.hat