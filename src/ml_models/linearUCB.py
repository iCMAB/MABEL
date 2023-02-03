import csv

import numpy as np
import pandas
import random
from scipy.linalg import inv
import dataset
import math

# # number of arms
# n_arms = 4
# # dimension of feature vector
# d = 4
# # initialization of A matrix
# A = [np.eye(d) for _ in range(n_arms)]
# # initialization of b vector
# b = np.array([np.zeros(d) for _ in range(n_arms)])


# def update(arm, x, reward):
#     A[arm] += np.outer(x, x)
#     b[arm] += reward.dot(x)


# def select_arm(x, alpha=1.0):
#     theta = [np.dot(inv(A[a]), b[a]) for a in range(n_arms)]
#     p = [np.dot(theta[a], x) for a in range(n_arms)]
#     ucb = [p[a] + alpha * np.sqrt(np.dot(np.dot(x, inv(A[a])), x)) for a in range(n_arms)]
#     return np.argmax(ucb)

class LinearUCB:
    def __init__(self, d, alpha):
        self.d = d
        self.alpha = alpha
        self.A = [np.identity(d)] * 4
        self.b = [np.zeros((d, 1))] * 4
        self.theta = [np.zeros((d, 1))] * 4

    def select_arm(self, readings):
        # Calculate the upper confidence bound for each arm
        ucb = [0] * 3
        for i in range(3):
            theta = np.linalg.inv(self.A[i]).dot(self.b[i])
            x = np.array(readings[i]).reshape(-1, 1)
            ucb[i] = np.dot(theta.T, x) + self.alpha * math.sqrt(np.dot(x.T, np.linalg.inv(self.A[i]).dot(x)))

        # Select the arm with the highest upper confidence bound
        # print("UCB", ucb)
        return np.argmax(ucb)

    def update(self, arm, x, penalty):
        x = np.array(x).reshape(-1, 1)
        self.A[arm] += np.dot(x, x.T)
        self.b[arm] -= penalty * x
        self.theta[arm] = np.linalg.inv(self.A[arm]).dot(self.b[arm])
        # print("UPDATE", np.linalg.inv(self.A[arm]).dot(self.b[arm]))

# def main():
#     # number of time steps
#     T = 1000
#     # feature vector of the current context
#     path = "C:\\Users\\vvvar\\Varsha\\Artificial_Intelligence\\iCMAB-SimulationTool-main\\iCMAB-SimulationTool-main" \
#            "\\data\\acv_start.csv"
#     for t in range(T):
#         dists = np.array([random.uniform(0,20) for _ in range(n_arms)])
#         # select arm with highest UCB value
#         arm = select_arm(dists)
#         # observe reward from pulling arm
#         reward = np.array([0, 0, 0, 0])
#         update(arm, dists, reward)
#         print(reward)


# if __name__ == "__main__":
#     main()
