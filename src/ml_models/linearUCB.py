import numpy as np
from scipy.linalg import inv
import math

class LinearUCB:
    def __init__(self, d, alpha):
        self.d = d
        self.alpha = alpha
        self.A = [np.identity(d)] * 4
        self.b = [np.zeros((d, 1))] * 4
        self.theta = [np.zeros((d, 1))] * 4

    def select_arm(self, readings):
        # Calculate the upper confidence bound for each arm
        length = len(readings)
        ucb = [0] * length
        for i in range(length):
            # theta = np.linalg.inv(self.A[i]).dot(self.b[i])
            x = np.array(readings[i]).reshape(-1, 1)
            ucb[i] = np.dot(self.theta[i].T, x) + self.alpha * math.sqrt(np.dot(x.T, np.linalg.inv(self.A[i]).dot(x)))

        # Select the arm with the highest upper confidence bound
        return np.argmax(ucb)

    def update(self, arm, x, penalty):
        x = np.array(x).reshape(-1, 1)
        self.A[arm] += np.dot(x, x.T)
        self.b[arm] -= penalty * x
        self.theta[arm] = np.linalg.inv(self.A[arm]).dot(self.b[arm])
