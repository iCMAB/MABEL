import numpy as np

class BernoulliEpsilon:
    def __init__(self, d, epsilon):
        self.epsilon = epsilon
        self.d  = d
        self.values = [np.identity(d)] * 4

    def select_arm(self):
        if np.random.rand() < self.epsilon:
            # Explore: Choose a random arm with probability epsilon
            return np.random.randint(len(self.values))
        else:
            # Exploit: Choose the arm with the highest estimated value
            return np.argmax(self.values)

    def update(self, arm, reward):
        self.values[arm] += (reward - self.values[arm]) / (reward + 1)
