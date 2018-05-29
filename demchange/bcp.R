## this is bayesian analysis NOT online detection.

# install.packages("bcp")
##### univariate sequential data #####
# an easy problem with 2 true change points
library("bcp")
set.seed(5)
x <- c(rnorm(50), rnorm(10, 5, 1), rnorm(50))
bcp.1a <- bcp(x)
plot(bcp.1a, main="Univariate Change Point Example")
# legacyplot(bcp.1a)
# a hard problem with 1 true change point
# set.seed(5)
# x <- rep(c(0,1), each=50)
# y <- x + rnorm(50, sd=1)
# bcp.1b <- bcp(y)
# plot(bcp.1b, main="Univariate Change Point Example")