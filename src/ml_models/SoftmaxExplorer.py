from functools import reduce
import numpy as np
import random

from ml_models.MABModel import MABModel


class SoftmaxExplorer(MABModel):
    # theta - penalty calculator
    def __init__(self, **kwargs):
        self.n_arms = kwargs.get('n_arms')
        self.d = kwargs.get('d')
        # Epsilon is the probability with which an arm is selected.
        self.epsilon = kwargs.get('epsilon')
        self.counts = [np.zeros(self.d)] * self.n_arms

        # Intially all arms have the same penalties.
        self.theta = [np.zeros(self.d)] * self.n_arms

    # Selection of the arm happens using epsilon-greedy strategy
    def select_arm(self, **kwargs):
        z = np.sum(np.exp([x//self.epsilon for x in self.theta]))
        probs = np.exp([x//self.epsilon for x in self.theta]) / z
        print("probs are : ")
        flattenedArr = []
        for item in probs:
            for val in item:
                flattenedArr.append(val)
        return np.random.choice(self.n_arms, p=flattenedArr)

    # Updating of values happens using penalty values
    # Method takes as input the index of the arm that was played and the observed penalty,
    # and updates the estimated value of that arm using the formula for a sample mean.
    def update(self, **kwargs):
        arm = kwargs.get('arm')
        penalty = kwargs.get('penalty')
        self.counts[arm] += 1
        n = self.counts[arm]
        value = self.theta[arm]
        new_value = ((n - 1) / n) * value + (1 / n) * penalty
        self.theta[arm] = new_value