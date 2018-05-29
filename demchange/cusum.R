# Example of a change in mean at 100 in simulated normal data
set.seed(1)
x=c(rnorm(100,0,1),rnorm(100,10,1))
m.cusum=cpt.mean(x,penalty="Manual",pen.value=0.8,method="PELT",test.stat="CUSUM")
# plot(m.cusum, type = "l", cpt.col = "blue", xlab = "Index", cpt.width = 4)
# returns 101 as the changepoint location
cpts(m.cusum)
