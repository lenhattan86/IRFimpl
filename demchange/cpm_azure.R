library("cpm")
rows = read.csv("/home/tanle/projects/AzurePublicDataset/cpu_utils_86400.csv")
x = rows[,4000]
result <- processStream(x,"GLR",ARL0=500,startup=50)
plot(x, type='l',ylim=c(0,max(x)))
xlab="hours"
for (i in 1:length(result$changePoints)) {
    abline(v=result$changePoints[i], lty=2)
}