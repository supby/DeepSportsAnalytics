library(boot)
library(nnet)

# load data
d <- read.csv("../nhl_2014-2015.csv")

smp_size <- floor(0.75 * nrow(d))
set.seed(42)

train_ind <- sample(seq_len(nrow(d)), size = smp_size)

d.train <- data.frame(d[train_ind, ])

d.test <- data.frame(d[-train_ind, ])
#d.test <- !is.na(d.test)

model <- nnet(y~., data=d.train, size=35, decay=0.0001, maxit=2000, MaxNWts=10000)
results <- predict(model, d.test)

table(results, d.test$y)

n_score <- 0
test_count <- length(results)
for (i in 1:test_count) {
  if(d.test[i,"y"] == round(results[i]))
    n_score <- n_score + 1
}
print((n_score/test_count)*100)