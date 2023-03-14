# FunProjects

## 2023_poker.py:
Simulates a Texas Hold'em poker game.
Creates a card object with value/color and a deck.
Then shuffles the deck and simulates random assignment N times.
The code compares the value of hands and the table.
Returns a DataFrame object with a result (winning = 1, draw = 0.5, loss = 0).

### Result
![ezcv map](https://github.com/guerreroda/FunProjects/blob/main/poker_heatmap.png)


## 2018_Queue.R:
This R script simulates a poisson DGP of shopping or retail queue. It is useful to estimate processes where retailers need to optimize or open new cashiers. 
Simulete a queue of 1000 customers 1000 times with parameters 0.25 for arrival rate and 0.33 for service rate. Following the M/M/1 process, the arrival function follows a poisson distribution, the service function is exponential, and there is only one server available. We simulate the inter-arrival time with an exponential function, due to the relationship between poisson and exponential distributions.
The first part of the code is a queue generation function, given the parameters above, with N (1,000) customers. For each customer there is an inter-arrival time, following an exponential distribution, and a service-time following also an exponential distribution. Each customer is served after the previous customer fulfills his service time, i.e. after the ending time of each customer, generating a waiting-time greater or equal than zero. In general, our simulation generates time intervals from exponential distributions, and adds them up in a time-line. The last part of the code runs this queue generation function 100 times.

### Result

![ezcv map](https://github.com/guerreroda/FunProjects/blob/main/2018_Qmodel.jpg)

## 2018_Markov.R:

Consider a Markov Chain process where days transition between Sunny, Cloudy or Rainny with a probability that depends on the current weather. The probability of a sunny day followed by two cloudy days is estimated by calculating the process through the Markov chain:

$P(X_2=C,X_1=C│X_0=S)=P(X_1=C|X_0=S∩X_2=C|X_1=C)=0.2*0.5 = 0.1 $

Mean length of a rainy period refers to the sojourn time or holding time of the rainy state.

$E(R)=1/(1-P(X_1=R|X_0=R))=1/(1-0.2)=1/0.8=1.25 $

To simulate 10,000 times the process we create a function to generate days in R following the markov chain previously stated. The function takes the current state ($X_0$), the available states ${S=1,C=2,R=3}$ and the probability matrix ($P$). Following these arguments, we use the sample built-in function in R to take a day out of the states given the current day and the probabilities in the current-state row. Once prepared this function, we introduce it in the loops that iterate each simulation.

### Result

![ezcv map](https://github.com/guerreroda/FunProjects/blob/main/2018_MarkovFig.jpg)

Simulation of two cloudy days after a sunny day.
