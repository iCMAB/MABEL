import numpy as np
import math

from ml_models.MABModel import MABModel

class LinearUCB(MABModel):
    def __init__(self, **kwargs):
        self.n_arms = kwargs.get('n_arms')
        self.d = kwargs.get('d')
        self.alpha = kwargs.get('alpha')
        self.ideal_distance = kwargs.get('ideal_distance')
        
        self.A = [np.identity(self.d)] * self.n_arms
        self.b = [np.zeros((self.d, 1))] * self.n_arms
        self.theta = [np.zeros((self.d, 1))] * self.n_arms

    def select_arm(self, **kwargs):
        variations = kwargs.get('variations')

        # Calculate the upper confidence bound for each arm
        length = self.n_arms
        ucb = [0] * length
        for i in range(length):
            # theta = np.linalg.inv(self.A[i]).dot(self.b[i])
            x = np.array(variations[i]).reshape(-1, 1)
            ucb[i] = np.dot(self.theta[i].T, x) + self.alpha * math.sqrt(np.dot(x.T, np.linalg.inv(self.A[i]).dot(x)))

        # Select the arm with the highest upper confidence bound
        return np.argmax(ucb)

    def update(self, **kwargs):
        arm = kwargs.get('arm')
        x = kwargs.get('x')
        penalty = kwargs.get('penalty')

        x = np.array(x).reshape(-1, 1)
        self.A[arm] = self.A[arm] + np.dot(x, x.T)
        self.b[arm] = self.b[arm] + (penalty * x.reshape(-1)) # Subtraction changed to addition
        self.theta[arm] = np.linalg.inv(self.A[arm]).dot(self.b[arm])
