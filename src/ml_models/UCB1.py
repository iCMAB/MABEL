import numpy as np
import random

import numpy as np


class UCB1:
    def __init__(self, n_arms, d):
        self.n_arms = n_arms
        self.d = d
        self.total_selections = 0
        # Total reward from each arm
        self.total_rewards = np.zeros(n_arms)
        # Number of times each arm has been selected
        self.num_selections = np.zeros(n_arms)
        # Feature vector
        self.arm_features = np.zeros((n_arms, d))

    def update(self, arm, reward, x):
        """
        Update the statistics for arm with observed reward and feature vector `x`.
        """
        self.total_rewards[arm] += reward 
        self.num_selections[arm] += 1
        self.arm_features[arm] = x

    def select_arm(self):
        """
        Choose the arm with the highest UCB val based on the current estimates of the mean reward and variance.
        """
        if self.total_selections < self.n_arms:
            # If fewer than `n_arms` selections have been made, simply choose the next arm in sequence
            arm = self.total_selections
        else:
            # Otherwise, calculate the UCB values for each arm and choose the arm with the highest value
            ucb_values = self.total_rewards / self.num_selections + \
                np.sqrt(2 * np.log(self.total_selections) / self.num_selections)
            arm = np.argmax(ucb_values)
        self.total_selections += 1 
        return arm


    # def __init__(self, d, epsilon):
    #     self.epsilon = epsilon
    #     self.d = d
    #     self.values = [np.identity(d)] * 4

    # def select_arm(self):
    #     myRandVal = random.uniform(0, 1)
    #     if myRandVal < self.epsilon:
    #         print("i'm exploring")
    #         # Explore: Choose a random arm with probability epsilon
    #         return np.random.randint(0, len(self.values)-1)
    #     else:
    #         print("i'm exploiting")
    #         # Exploit: Choose the arm with the highest estimated value
    #         return np.argmax(self.values)

    # def update(self, arm, reward):
    #     self.values[arm] += (reward - self.values[arm]) / (reward + 1)
