library(boot)
library(gbm)

# load data
d <- read.csv("../nhl_2014-2015.csv")
d <- d[,!(names(d) %in% c("x1"))]

smp_size <- floor(0.75 * nrow(d))
set.seed(42)

train_ind <- sample(seq_len(nrow(d)), size = smp_size)

d.train <- data.frame(d[train_ind, ])

d.test <- data.frame(d[-train_ind, ])

model <- gbm(y~., data=d.train, n.trees=100)

results <- predict(model, d.test, n.trees=100, type="response")

table(results, d.test$y)

n_score <- 0
test_count <- length(results)
for (i in 1:test_count) {
  if(d.test[i,"y"] == round(results[i]))
    n_score <- n_score + 1
}
print((n_score/test_count)*100)