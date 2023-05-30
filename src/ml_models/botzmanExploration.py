import numpy as np
from ml_models.MABModel import MABModel

class BoltzmanExploration(MABModel):
    def __init__(self, **kwargs):
        self.n_arms = kwargs.get('n_arms')
        self.temperature = kwargs.get('temperature')
        self.alpha = kwargs.get('alpha')

        self.reset()

    def reset(self):   
        self.q_estimates = np.zeros(self.n_arms)
        self.action_count = np.zeros(self.n_arms)

    def select_arm(self, **kwargs):
        boltzmann_probs = np.exp(self.q_estimates / self.temperature) / np.sum(np.exp(self.q_estimates / self.temperature))
        arm = np.random.choice(np.arange(self.n_arms), p=boltzmann_probs)
        return arm

    def update(self, **kwargs):
        arm = kwargs.get('arm')
        penalty = kwargs.get('penalty')
        self.action_count[arm] += 1
        alpha = 1 / self.action_count[arm]
        self.q_estimates[arm] = (1 - alpha) * self.q_estimates[arm] + alpha * (penalty)

