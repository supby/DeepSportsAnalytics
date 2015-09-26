require(graphics)

d <- read.csv("../nhl_2014-2015.csv")

pc.cr <- princomp(~.,data=d)

summary(pc.cr)
loadings(pc.cr)
plot(pc.cr)
biplot(pc.cr)
