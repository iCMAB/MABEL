import numpy as np

class LinearThompsonSampling:
    def __init__(self, d):
        self.d = d
        # Covariance matrix, initialized as identity matrix
        self.A = np.identity(d)
        self.b = np.zeros(d)  # Observation vector, initialized as zero vector

    def update(self, x, reward):
        x = x.reshape(-1, self.d)
        self.A += np.dot(x.T, x)  # Update covariance matrix
        self.b += reward * x.reshape(-1)  # Update observation vector

    def choose_arm(self, x):
        x = x.reshape(-1, self.d)
        theta_samples = np.random.multivariate_normal(
            np.linalg.inv(self.A).dot(self.b), np.linalg.inv(self.A), size=1)
        # Calculate the mean of the estimated rewards for each arm
        means = x.dot(theta_samples.T)
        # Choose the arm with the maximum estimated reward
        return np.argmax(means)
