import numpy as np
from scipy.linalg import inv

class LinearThompsonSampling:
    def __init__(self, d):
        self.d = d
        # Covariance matrix, initialized as identity matrix
        self.A = [np.identity(d)] * 4
        self.means = [np.identity(d)] * 4
        self.b = [np.zeros((d, 1))] * 4  # Observation vector, initialized as zero vector
        self.theta = [np.zeros((d, 1))] * 4
        self.var = [np.zeros((d, 1))] * 4

    def update(self, arm, x, reward):
        x = np.array(x).reshape(-1, 1)
        self.A[arm] += np.dot(x, x.T)  # Update covariance matrix
        self.b[arm] += reward * x.reshape(-1)  # Update observation vector
        self.theta[arm] = np.linalg.inv(self.A[arm]).dot(self.b[arm])


    def select_arm(self, readings):
        theta = np.random.normal(self.means, np.sqrt(self.var))
        return np.argmax(theta)
