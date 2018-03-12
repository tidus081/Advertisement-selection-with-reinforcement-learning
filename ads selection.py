
"""
we are finding strategy how we choose one ad to display to users each time
they connect to a web page
Which ad is
Random selection
Upper Confidence Bound Algorithm
Thompson sampling
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

# customer simulation data which expect that customers click some ads. 
dataset = pd.read_csv('Ads.csv') 


# Implementing Random Selection 
import random
N = 10000
d=10

ads_selected_random = []
total_reward = 0

for n in range(0,N):
    ad = random.randrange(d)
    ads_selected_random.append(ad)
    reward = dataset.values[n,ad]
    total_reward += reward

plt.hist(ads_selected_random)
plt.title('Histogram of ads selection in Random sample')
plt.show()

# Implementing Upper Confidence Bound Algorithm
"""
step1 
At each round n, we consider two numbers for each ad i
Ni(n) - the number of times the ad i was selected
Ri(n) - the sum of rewards of the ad i

#step2
# the average reward of ad i up to round n
# ri(n) = Ri(n)/Ni(n)
# confidence interval [ri(n)-deltai(n),ri(n)+deltai(n)]
# deltai(n)=sqrt(3log(n)/2Ni(n))

# step3 
We select the ad i which has max UCB ri(n)+delta(n)

"""
numbers_of_selections = [0]*d
sums_of_rewards = [0]*d
ads_selected_UCB = []
total_reward = 0

for n in range(0,N):
    max_upper_bound = 0
    ad = 0
    for i in range(0,d):
        if (numbers_of_selections[i] >0):
            average_reward = sums_of_rewards[i] / numbers_of_selections[i]
            delta_i = math.sqrt(3/2 * math.log(n+1)/numbers_of_selections[i] )
            upper_bound = average_reward + delta_i
        else:
            upper_bound = 1e4000
        if upper_bound > max_upper_bound:
            max_upper_bound = upper_bound
            ad = i  
    ads_selected_UCB.append(ad)
    numbers_of_selections[ad]+=1
    reward = dataset.values[n,ad]
    sums_of_rewards[ad]+=reward
    total_reward = total_reward + reward

plt.hist(ads_selected_UCB)
plt.title('Histogram of ads selections in UCB')
plt.xlabel('Ads')
plt.ylabel('Number of times each ad was selected')
plt.show()

# Implementing Thompson sampling
"""
generally Thompson sampling is better than UCB
step1
N1i(n) - the number of times the ad i got reward 1 up to round n
N0i(n) - the number of times the ad i got reward 0 up to round n

step2
For each ad i, we take a random draw from the distribution below
0i(n) = B(n1i(n) +1,N0i(n)+1)

step3
we select the ad that has the highest 0i(n)
"""

numbers_of_rewards_1 = [0]*d
numbers_of_rewards_0 =  [0]*d
sums_of_rewards = [0]*d
ads_selected_Thompson = []
total_reward = 0

for n in range(0,N):
    max_random_draw = 0
    ad = 0
    for i in range(0,d):
        random_beta = random.betavariate(numbers_of_rewards_1[i]+1,numbers_of_rewards_0[i]+1)
        if random_beta > max_random_draw:
            max_random_draw = random_beta
            ad = i  
    ads_selected_Thompson.append(ad)
    reward = dataset.values[n,ad]
    if reward==1:
        numbers_of_rewards_1[ad] +=1
    else:
        numbers_of_rewards_0[ad] +=1
    total_reward = total_reward + reward
    
plt.hist(ads_selected_Thompson)
plt.title('Histogram of ads selections in Thompson sampling')
plt.xlabel('Ads')
plt.ylabel('Number of times each ad was selected')
plt.show()

s = pd.DataFrame(data = {"Random" : ads_selected_random, "UCB": ads_selected_UCB, "Thompson": ads_selected_Thompson})
s[0:20]

    
