import numpy as np
from ml_models.MABModel import MABModel


class BootstrappedUCB(MABModel):
    def __init__(self, **kwargs):
        self.n_arms = kwargs.get('n_arms')
        self.n_bootstrap = kwargs.get('n_bootstrap')
        self.alpha = kwargs.get('alpha')

        self.reset()

    def reset(self):
        self.t = 0
        self.penaltyVals = [[0] for _ in range(self.n_arms)]
        self.means = np.zeros(self.n_arms)
        self.theta = np.zeros(self.n_arms)
        self.n_pulls = np.zeros(self.n_arms)
        self.bootstrap_means = np.zeros((self.n_arms, self.n_bootstrap))

    def select_arm(self, **kwargs):
        variations = kwargs.get('variations')

        if self.t < self.n_arms:
            arm = self.t
        else:
            upper_confidence_bounds = [0] * self.n_arms
            bootstrap_upper_confidence_bounds = [0] * self.n_arms

            for i in range(self.n_arms):
                x = np.array(variations[i]).reshape(-1, 1)
                upper_confidence_bounds[i] = np.dot(self.means[i].T, x) + \
                    np.sqrt(self.alpha * np.log(self.t + 1) / self.n_pulls[i])

                bootstrap_upper_confidence_bounds[i] = np.percentile(
                    self.bootstrap_means[i], q=100 * (1-1/(self.t+1)))

                upper_confidence_bounds[i] += bootstrap_upper_confidence_bounds[i]

            arm = np.argmax(upper_confidence_bounds)
        
        self.t += 1
        return arm

    def update(self, **kwargs):
        arm = kwargs.get('arm')
        penaltyVal = kwargs.get('penalty')

        self.penaltyVals[arm].append(penaltyVal)
        self.n_pulls[arm] += 1
        self.means[arm] = np.mean(self.penaltyVals[arm])

        bootstrap_indices = np.random.randint(low=0, high=len(
            self.penaltyVals[arm]), size=(self.n_bootstrap,))
        bootstrap_samples = np.array(self.penaltyVals[arm])[bootstrap_indices]
        bootstrap_means = np.mean(bootstrap_samples)
        self.bootstrap_means[arm, :] = bootstrap_means

        self.theta[arm] = self.means[arm]
