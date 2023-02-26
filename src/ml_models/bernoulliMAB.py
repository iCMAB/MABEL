import numpy as np
import random

class BernoulliEpsilon:
    # theta - penalty calculator
    def __init__(self, d, epsilon):
        self.epsilon = epsilon
        self.d  = d
        self.theta = [np.identity(d)] * 4

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

    def update(self, arm, readingsVal, penalty):
        self.theta[arm] += (penalty - self.theta[arm]) / (penalty + 1)
