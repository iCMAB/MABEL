from functools import reduce
import numpy as np
import random

from ml_models.MABModel import MABModel


class SoftmaxExplorer(MABModel):
    def __init__(self, **kwargs):
        self.n_arms = kwargs.get('n_arms')
        self.d = kwargs.get('d')

        # Epsilon is the probability with which an arm is selected.
        self.epsilon = kwargs.get('epsilon')
        self.counts = [np.zeros(self.d)] * self.n_arms

        # Intially all arms have the same penalties.
        self.values = [np.ones(self.d)] * self.n_arms
        self.theta = self.values

    def select_arm(self, **kwargs):
        variations = kwargs.get('variations')

        z = np.sum(np.exp([np.dot(x, variations[i]) // self.epsilon for i, x in enumerate(self.values)]))
        probs = np.exp([np.dot(x, variations[i]) // self.epsilon for i, x in enumerate(self.values)]) / z

        flattenedArr = []
        for item in probs:
            for val in item:
                flattenedArr.append(val)
            
        return np.random.choice(self.n_arms, p=flattenedArr)

    def update(self, **kwargs):
        arm = kwargs.get('arm')
        penalty = kwargs.get('penalty')

        self.counts[arm] += 1
        n = self.counts[arm]
        value = self.values[arm]
        new_value = ((n - 1) / n) * value + (1 / n) * penalty
        self.values[arm] = new_value
        
        self.theta = self.values
