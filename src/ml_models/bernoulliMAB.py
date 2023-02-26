import numpy as np
import random

class BernoulliEpsilon:
    # theta - penalty calculator
    def __init__(self, d, epsilon):
        # Epsilon is the probability with which an arm is selected.
        self.epsilon = epsilon
        self.d  = d
        # Intially all arms have the same penalties.
        self.theta = [np.identity(d)] * 4

    # Selection of the arm happens using epsilon-greedy strategy
    def select_arm(self):
        myRandVal = random.uniform(0,1)
        if myRandVal < self.epsilon:
            print("i'm exploring")
            # Explore: Choose a random arm with probability epsilon
            return np.random.randint(0,len(self.theta)-1)
        else:
            print("i'm exploiting")
            # Exploit: Choose the arm with the highest estimated value
            return np.argmax(self.theta)

    #Updating of values happens using penalty values
    # method takes as input the index of the arm that was played and the observed penalty, 
    # and updates the estimated value of that arm using the formula for a sample mean.
    def update(self, arm, readingsVal, penalty):
        self.theta[arm] += (penalty - self.theta[arm]) / (penalty + 1)
