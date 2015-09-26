library(boot)
library(mda)
library(MASS)

# load data
d <- read.csv("../nhl_2014-2015.csv")
#d <- d[,!(names(d) %in% c("x1"))]

smp_size <- floor(0.75 * nrow(d))
set.seed(42)

train_ind <- sample(seq_len(nrow(d)), size = smp_size)

d.train <- data.frame(d[train_ind, ])

d.test <- data.frame(d[-train_ind, ])
d.test <- !is.na(d.test)

model <- mda(y ~ ., data = d.train)
#model <- qda(y ~ ., data = d.train)
results <- predict(object = model, newdata = d.test)

table(results, d.test$y)
