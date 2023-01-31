import csv

import numpy as np
import pandas
from scipy.linalg import inv

# number of arms
n_arms = 4
# dimension of feature vector
d = 4
# initialization of A matrix
A = [np.eye(d) for _ in range(n_arms)]
# initialization of b vector
b = [np.zeros(d) for _ in range(n_arms)]


def update(arm, x, reward):
    A[arm] += np.outer(x, x)
    b[arm] += reward * x


def select_arm(x, alpha=1.0):
    theta = [np.dot(inv(A[a]), b[a]) for a in range(n_arms)]
    p = [np.dot(theta[a], x) for a in range(n_arms)]
    ucb = [p[a] + alpha * np.sqrt(np.dot(np.dot(x, inv(A[a])), x)) for a in range(n_arms)]
    return np.argmax(ucb)


def main():
    # number of time steps
    T = 1000
    # feature vector of the current context
    path = "C:\\Users\\vvvar\\Varsha\\Artificial_Intelligence\\iCMAB-SimulationTool-main\\iCMAB-SimulationTool-main" \
           "\\data\\acv_start.csv"
    featureDf = pandas.read_csv(path)
    for t in range(T):
        # select arm with highest UCB value
        arm = select_arm(featureDf)
        # observe reward from pulling arm
        reward = [0, 0, 0, 0]
        update(arm, featureDf, reward)
        print(reward)


if __name__ == "__main__":
    main()
