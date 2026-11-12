ad <- c(13,	8, 10,	15,	12,	15,	14,	15,	17,	19,	20,	21,	22,	21,	25)
sales <- c(94, 70,	90,	100,	95,	100,	85,	95,	105,	105,	110,	105,	104,	105,	121)

lm(sales ~ ad)

linmod1 <- lm(sales ~ ad)
summary(linmod1)
fit <- lm(sales ~ ad)



plot(linmod1)















