library(boot)

# load data
d <- read.csv("../nhl_2014-2015.csv")

smp_size <- floor(0.75 * nrow(d))
set.seed(42)

train_ind <- sample(seq_len(nrow(d)), size = smp_size)

d.train <- data.frame(d[train_ind, ])
d.test <- data.frame(d[-train_ind, ])

# train linear model
glm.fit <- glm(y~., data = d.train)

# calculate mean error

# paste(predict(glm.fit, d.test, type="response")[1])

# paste("mean error =", sqrt(mean((d.test["target"] - predict(glm.fit, d.test, type="response"))^2))

# use 10-fold
#cv.err <- cv.glm(d.train, glm.fit, K=10)
#paste("cv.err$delta:", cv.err$delta)

p <- predict(glm.fit, d.test, type="response")
n_score <- 0
test_count <- length(p)
for (i in 1:test_count) {
  if(d.test[i,"y"] == round(p[i]))
    n_score <- n_score + 1
}
print((n_score/test_count)*100)
