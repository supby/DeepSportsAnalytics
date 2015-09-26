library(boot)
library(neuralnet)

# load data
d <- read.csv("../nhl_2014-2015.csv")

smp_size <- floor(0.75 * nrow(d))
set.seed(42)

train_ind <- sample(seq_len(nrow(d)), size = smp_size)
d.train <- data.frame(d[train_ind, ])
d.test <- data.frame(d[-train_ind, ])

model <- neuralnet(y~x0+x1+x2+x3+x4+x5+x6+x7+x8+x9+x10+x11+x12+x13+x14+x15+x16+x17+x18+x19+x20+x21+x22+x23+x24, d.train, hidden=10)
#plot(model)
results <- compute(model, subset(d.test, select = c("x0","x1","x2","x3","x4","x5","x6","x7","x8","x9","x10","x11","x12","x13","x14","x15","x16","x17","x18","x19","x20","x21","x22","x23","x24")))

n_score <- 0
test_count <- length(results$net.result)
for (i in 1:test_count) {
  if(d.test[i,"y"] == round(results$net.result[i]))
    n_score <- n_score + 1
}
print((n_score/test_count)*100)



