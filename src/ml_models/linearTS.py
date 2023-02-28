import numpy as np
from scipy.linalg import inv

from ml_models.MABModel import MABModel

class LinearThompsonSampling(MABModel):
    def __init__(self, **kwargs):
        self.iteration = 1
        self.d = kwargs.get('d')
        # Covariance matrix, initialized as identity matrix
        self.var = [np.identity(self.d)] * 3
        self.means = [np.identity(self.d)] * 3
        self.b = [np.zeros((self.d, 1))] * 3  # Observation vector, initialized as zero vector
        self.theta = [np.zeros((self.d, 1))] * 3

    def select_arm(self, **kwargs):
        theta = np.random.normal(self.means, np.sqrt(self.var))
        return np.argmax(theta)

    def update(self, **kwargs):    
        arm = kwargs.get('arm')
        x = kwargs.get('x')
        penalty = kwargs.get('penalty')

        x = np.array(x).reshape(-1, 1)
        self.var[arm] = self.var[arm] + np.dot(x, x.T)  # Update covariance matrix
        self.b[arm] = self.b[arm] - (penalty * x.reshape(-1))  # Update observation vector
        self.theta[arm] = np.linalg.inv(self.var[arm]).dot(self.b[arm])
        
        # update self.means
        self.means[arm]=(self.b[arm]-self.means[arm])/self.iteration
        self.iteration+=1



    
