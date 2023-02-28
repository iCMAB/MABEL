import numpy as np

class UCB1:
    def __init__(self, d, n_arms, alpha):
        self.n_arms = n_arms
        self.d = d
        self.total_selections = 0
        self.total_rewards = np.zeros(n_arms)
        self.num_selections = np.zeros(n_arms)
        self.arm_features = np.zeros((n_arms, d))

    def update(self, arm, reward, x):
        """
        Update the statistics for arm with observed reward and feature vector `x`.
        """
        self.total_rewards[arm] = self.total_rewards[arm] + reward
        self.num_selections[arm] = self.num_selections[arm] + 1
        self.arm_features[arm] = x

    def select_arm(self):
        """
        Choose the arm with the highest UCB val based on the current estimates of the mean reward and variance.
        """
        # Try each arm
        if self.total_selections < self.n_arms:
            arm = self.total_selections
        else:
            #  Then calculate UCB value for each arm and choose the arm with the highest value
            ucb_values = self.total_rewards / self.num_selections + \
                np.sqrt(2 * np.log(self.total_selections) / self.num_selections)
            arm = np.argmax(ucb_values)
        self.total_selections += 1 
        return arm
