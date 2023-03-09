import numpy as np
import random

from ml_models.MABModel import MABModel


class EpsilonGreedy(MABModel):
    # theta - penalty calculator
    def __init__(self, **kwargs):
        self.n_arms = kwargs.get('n_arms')

        # Epsilon is the probability with which an arm is selected.
        self.epsilon = kwargs.get('epsilon')
        self.d = kwargs.get('d')

        # Intially all arms have the same penalties.
        self.theta = [np.identity(self.d)] * self.n_arms

    # Selection of the arm happens using epsilon-greedy strategy
    def select_arm(self, **kwargs):
        rand_val = random.uniform(0, 1)
        if rand_val < self.epsilon:
            # Explore: Choose a random arm with probability epsilon
            return np.random.randint(0, len(self.theta))
        else:
            # Exploit: Choose the arm with the highest estimated value
            return np.argmax(self.theta)

    # Updating of values happens using penalty values
    # Method takes as input the index of the arm that was played and the observed penalty,
    # and updates the estimated value of that arm using the formula for a sample mean.
    def update(self, **kwargs):
        arm = kwargs.get('arm')
        penalty = kwargs.get('penalty')

        self.theta[arm] = self.theta[arm] + \
            ((penalty - self.theta[arm]) / (penalty + 1))
