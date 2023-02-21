import numpy as np

class LinearThompsonSampling:
    def __init__(self, d):
        self.iteration = 1
        self.d = d
        # Covariance matrix, initialized as identity matrix
        self.var = [np.identity(d)] * 3
        self.means = [np.identity(d)] * 3
        self.b = [np.zeros((d, 1))] * 3  # Observation vector, initialized as zero vector
        self.theta = [np.zeros((d, 1))] * 3

    def update(self, arm, x, reward):        
        x = np.array(x).reshape(-1, 1)
        self.var[arm] += np.dot(x, x.T)  # Update covariance matrix
        self.b[arm] += reward * x.reshape(-1)  # Update observation vector
        self.theta[arm] = np.linalg.inv(self.var[arm]).dot(self.b[arm])
        # update self.means
        self.means[arm]=(self.b[arm]-self.means[arm])/self.iteration
        self.iteration+=1
        # print(self.iteration)



    def select_arm(self):
        theta = np.random.normal(self.means, np.sqrt(self.var))
        return np.argmax(theta)
