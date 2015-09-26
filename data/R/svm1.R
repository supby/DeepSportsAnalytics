library(boot)
library(e1071)
#library(printr)

# load data
d <- read.csv("../nhl_2014-2015.csv")
d <- d[,!(names(d) %in% c("x1"))]
#d[,"y"] <- as.factor(d[,"y"])

smp_size <- floor(0.75 * nrow(d))
set.seed(42)

train_ind <- sample(seq_len(nrow(d)), size = smp_size)

d.train <- data.frame(d[train_ind, ])
d.test <- data.frame(d[-train_ind, ])
#d.test <- !is.na(d.test)

# train linear model
model <- svm(y ~ ., data = d.train)
results <- predict(object = model, newdata = d.test, type = "class")

table(results, d.test$y)

n_score <- 0
test_count <- length(results)
for (i in 1:test_count) {
  #if(d.test[i,"y"] == results[i])  
  if(d.test[i,"y"] == round(results[i]))
    n_score <- n_score + 1
}
print((n_score/test_count)*100)
