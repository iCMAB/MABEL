import numpy as np

class LinUCB:
    def __init__(self, d, alpha):
        self.d = d
        self.alpha = alpha
        self.A = [np.identity(d) for i in range(4)]
        self.b = [np.zeros(d) for i in range(4)]
        self.theta = [np.zeros(d) for i in range(4)]
        
    def select_arm(self, x):
        ucb = [np.dot(self.theta[i], x) + self.alpha * np.sqrt(np.dot(x, np.dot(np.linalg.inv(self.A[i]), x))) for i in range(4)]
        return np.argmax(ucb)
    
    def update(self, i, x, reward):
        self.A[i] += np.outer(x, x)
        self.b[i] += reward * x
        self.theta[i] = np.dot(np.linalg.inv(self.A[i]), self.b[i])

# Example usage
d = 3
alpha = 0.1
model = LinUCB(d, alpha)

# Create context vectors
X = [np.array([1, 1, 1]), np.array([2, 2, 2]), np.array([3, 3, 3]), np.array([4, 4, 4])]

# Create array of distance values
readings = [1.5, 2.5, 3.5]

# Run LinUCB for T timesteps
T = 100
bad_sensors = []
for t in range(T):
    # Select an arm (ACV) to query
    i = model.select_arm(X[t % 4])
    
    # Observe the reward (distance value) from the selected ACV
    r = readings[i]
    
    # Update the model
    model.update(i, X[i], r)
    
    # Check if the residual is larger than a threshold
    residual = abs(r - np.dot(model.theta[i], X[i]))
    if residual > 0.1:
        bad_sensors.append(i)
        
print("Bad sensors:", bad_sensors)