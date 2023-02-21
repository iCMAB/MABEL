import numpy as np

class BernoulliEpsilon:
    def __init__(self, epsilon):
        self.epsilon = epsilon
        self.values = []

    def initialize(self, num_arms):
        self.values = np.zeros(num_arms)

    def select_arm(self):
        if np.random.rand() < self.epsilon:
            # Explore: Choose a random arm with probability epsilon
            return np.random.randint(len(self.values))
        else:
            # Exploit: Choose the arm with the highest estimated value
            return np.argmax(self.values)

    def update(self, arm, reward):
        self.values[arm] += (reward - self.values[arm]) / (self.num_pulls[arm] + 1)
