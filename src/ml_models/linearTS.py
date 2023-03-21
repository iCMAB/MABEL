import numpy as np

from ml_models.MABModel import MABModel

class LinearThompsonSampling(MABModel):
    def __init__(self, **kwargs):
        self.n_arms = kwargs.get('n_arms')
        self.iteration = 1
        self.d = kwargs.get('d')
        self.ideal_distance = kwargs.get('ideal_distance')

        # Covariance matrix, initialized as identity matrix
        self.var = [np.identity(self.d)] * self.n_arms
        self.means = [np.identity(self.d)] * self.n_arms
        self.b = [np.zeros((self.d, 1))] * self.n_arms  # Observation vector, initialized as zero vector
        self.theta = [np.zeros((self.d, 1))] * self.n_arms

    def select_arm(self, **kwargs):
        variations = kwargs.get('variations')
            
        theta = np.random.normal(self.means, np.sqrt(self.var))

        for i in range(self.n_arms):
            x = np.array(variations[i]).reshape(-1, 1)
            theta[i] = np.abs(np.dot(theta[i], x.T))

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



    
