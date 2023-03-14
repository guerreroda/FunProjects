# Disable scientific notation from graphs.
options(scipen=999)

# For exercise 9.3.1, use R to simulate a Markov chain and estimate the probabilities
# in part (a) and part (b), and the mean in part (c)
# The following matrix is the single-step transition probability matrix of a discrete-time Markov chain
# which describes the weather. State 1 represents a sunny day, state 2 a cloudy day, and state 3 a rainy day.
#   S   C    R
# S .7  .2  .1
# C .3  .5  .2
# R .2  .6  .2
P = matrix(c(.7, .2, .1, .3, .5, .2, .2, .6, .2), nrow=3, byrow = TRUE)
# (a) What is the probability of a sunny day being followed by two cloudy days?
# S=1, C=2, R=3
days = c(1,2,3)
# Generates the following day given a current day, sample of days, and a Transition Matrix
day_generator <- function(state, states, MarkovC){
  return(sample(states, prob=MarkovC[state,], size = 1))
}

N = 10000

# DF will take n simulations and probability.
df1 = data.frame(simuls=numeric(), p=numeric())
counter=0
week = c(1)
for(i in 1:N){
  # initial day is sunny
  day_2 <- day_generator(week[1],days,P)
  day_3 <- day_generator(day_2,days,P)
  if(day_2==2&day_3==2){counter=counter+1}
  df1 <- rbind(df1, data.frame(simuls=i, p=counter/i))
}

df1 <- df1[-c(seq(1:100)), ]
# plot a graph with simulations and probability.
plot(df1, type="l")
abline(h=0.1, lty=2, col = 2)

# (b) Given that today is rainy, what is the probability that the sun will shine the day after tomorrow?
# DF will take n simulations and probability.
df2 = data.frame(simuls=numeric(), p=numeric())
counter=0
week = c(3)
for(i in 1:N){
  # initial day is sunny
  day_2 <- day_generator(week[1],days,P)
  day_3 <- day_generator(day_2,days,P)
  if(day_3==1){counter=counter+1}
  df2 <- rbind(df2, data.frame(simuls=i, p=counter/i))
}

df2 <- df2[-c(seq(1:100)), ]
# plot a graph with simulations and probability.
plot(df2, type="l")
abline(h=.36, lty=2, col = 2)

# (c) What is the mean length of a rainy period?
df3 = data.frame(simuls=numeric(), p=numeric())
count = 0
for(n in 1:N){
  week = numeric(100)
  week[1] = 3
  for(i in 2:100){
    week[i] = day_generator(week[i-1],days,P)
  }
  for(i in week){
    if(i==3){count=count+1}
    else{break}
  }
  df3 <- rbind(df3, data.frame(simuls=n, p=count/n))
}
df3 <- df3[-c(seq(1:100)), ]
plot(df3, type="l")
abline(h=1.25, lty=2, col = 2)
