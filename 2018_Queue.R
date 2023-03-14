# Simulate an M/M/1 queue, assuming customers come according
# to a poisson process with rate 0.25 person per minute and the
# service time follows an exponential distribution with mean 3 minutes.
# Estimate the mean waiting time for the system

# make function with args lambda, mu and N that simulates queue.

queue_gen <- function(rate_arrival, rate_service, N_customers){
  # initial customer
  customer = 1
  time.arrival = 0
  # time interval: service
  int.service = rexp(1, rate=rate_service)
  # time interval: wait time.
  int.wait = 0
  # time service ends.
  time.end = int.service+time.arrival
  table = data.frame(customer, time.arrival, int.service, time.end, int.wait)
  # next customers
  while(customer<=(N_customers-1)) {
    customer = customer + 1
    int.arrival = rexp(1,rate=rate_arrival)
    time.arrival = time.arrival + int.arrival
    if(time.end - time.arrival>=0){
      int.wait = time.end - time.arrival
    }
    else{
      int.wait = 0
    }
    int.service = rexp(1, rate=rate_service)
    if(int.wait==0){
      time.end = time.arrival + int.service
    }
    else {
      time.end = time.end + int.service
    }
    table = rbind(table, data.frame(customer, time.arrival, int.wait, int.service, time.end))
  }
  return(mean(table$int.wait))
}


df = data.frame()
N = 100
for(i in 1:N) {
  df = rbind(df,
             data.frame(n=i,
                        mwt=queue_gen(rate_arrival = .25, rate_service = 1/3, N_customers = 1000))
                        )
}

plot(df, type="l")
summary(df)
