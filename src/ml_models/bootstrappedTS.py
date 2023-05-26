import numpy as np
from ml_models.MABModel import MABModel


class BootstrappedThompsonSampling(MABModel):
    def __init__(self, **kwargs):
        self.n_arms = kwargs.get('n_arms')
        self.n_bootstrap = kwargs.get('n_bootstrap')
        self.alpha = kwargs.get('alpha')
        self.d = kwargs.get('d')
        self.ideal_distance = kwargs.get('ideal_distance')

        self.reset()

    def reset(self):
        self.t = 0
        self.penaltyVals = [[0] for _ in range(self.n_arms)]
        self.means = np.zeros(self.n_arms)
        self.var = np.zeros(self.n_arms)
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
                theta_samples = np.random.normal(
                    loc=self.means[i], scale=np.sqrt(self.var[i]), size=self.n_bootstrap)
                bootstrap_samples = np.abs(
                    np.dot(variations[i], theta_samples.T))

                upper_confidence_bounds[i] = np.percentile(
                    bootstrap_samples, q=100*(1-1/(self.t+1)))

            arm = np.argmax(upper_confidence_bounds)

        self.t += 1
        return arm

    def update(self, **kwargs):
        arm = kwargs.get('arm')
        penaltyVal = kwargs.get('penalty')

        self.penaltyVals[arm].append(penaltyVal)
        self.n_pulls[arm] += 1
        self.means[arm] = np.mean(self.penaltyVals[arm])
        self.var[arm] = np.var(self.penaltyVals[arm])

        bootstrap_indices = np.random.randint(low=0, high=len(
            self.penaltyVals[arm]), size=(self.n_bootstrap,))
        bootstrap_samples = np.array(self.penaltyVals[arm])[bootstrap_indices]
        bootstrap_means = np.mean(bootstrap_samples)
        self.bootstrap_means[arm, :] = bootstrap_means

        self.theta[arm] = self.means[arm]
