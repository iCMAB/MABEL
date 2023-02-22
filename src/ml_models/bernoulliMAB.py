import numpy as np
import random

class BernoulliEpsilon:
    def __init__(self, d, epsilon):
        self.epsilon = epsilon
        self.d  = d
        self.values = [np.identity(d)] * 4

    def select_arm(self):
        myRandVal = random.uniform(0,1)
        if myRandVal < self.epsilon:
            print("i'm exploring")
            # Explore: Choose a random arm with probability epsilon
            return np.random.randint(0,len(self.values)-1)
        else:
            print("i'm exploiting")
            # Exploit: Choose the arm with the highest estimated value
            return np.argmax(self.values)

    def update(self, arm, reward):
        self.values[arm] += (reward - self.values[arm]) / (reward + 1)
