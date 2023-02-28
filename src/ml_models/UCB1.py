import numpy as np
from ml_models.MABModel import MABModel

"""Seeks to minimize penalty"""
class UCB1_Normal_Penalized(MABModel):
    def __init__(self, **kwargs):
        self.n_arms = kwargs.get('n_arms')
        self.d = kwargs.get('d')
        self.total_selections = 0
        self.theta = [np.identity(self.d)] * self.n_arms
        self.num_selections = [np.identity(self.d)] * self.n_arms

    def select_arm(self, **kwargs):
        """
        Choose the arm with the highest UCB val based on the current estimates of the mean reward and variance.
        """
        # Try each arm
        if self.total_selections < self.n_arms:
            arm = self.total_selections
        else:
            #  Then calculate UCB value for each arm and choose the arm with the smallest penalty
            ucb_values = []
            for i in range(len(self.theta)):
                ucb_values.append(self.theta[i] / self.num_selections[i] - np.sqrt(2 * np.log(self.total_selections) / self.num_selections[i]))
            arm = np.argmin(ucb_values)
        self.total_selections += 1
        return arm

    def update(self, **kwargs):
        """
        Update the statistics for arm with observed reward and feature vector `x`.
        """
        arm = kwargs.get('arm')
        penalty = kwargs.get('penalty')
        self.theta[arm] = self.theta[arm] + penalty
        self.num_selections[arm] = self.num_selections[arm] + 1