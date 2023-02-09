import numpy as np

class LinearThompsonSampling:
    def __init__(self, d):
        self.d = d
        # Covariance matrix, initialized as identity matrix
        self.A = [np.identity(d)] * 4
        self.b = [np.zeros((d, 1))] * 4  # Observation vector, initialized as zero vector
        self.theta = [np.zeros((d, 1))] * 4

    def update(self, arm, x, reward):
        x = np.array(x).reshape(-1, 1)
        self.A[arm] += np.dot(x, x.T)  # Update covariance matrix
        self.b[arm] += reward * x.reshape(-1)  # Update observation vector
        self.theta[arm] = np.linalg.inv(self.A[arm]).dot(self.b[arm])


    def select_arm(self, readings):
        # x = x.reshape(-1, self.d)
        length = len(readings)
        ts = [0] * length
        for i in range(length):
            x = np.array(readings[i]).reshape(-1, self.d)
            print(np.linalg.inv(self.A[i]).dot(
                self.b[i]))
            print(np.linalg.inv(self.A[i]))

            ts[i] = np.random.multivariate_normal(
                np.linalg.inv(self.A[i]).dot(self.b[i]), np.linalg.inv(self.A[i]), size=1)
        # Calculate the mean of the estimated rewards for each arm
            means = x.dot(ts[i].T)
        # Choose the arm with the maximum estimated reward
        return np.argmax(means)
