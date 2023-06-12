import random

import numpy as np

from .mab_model import MABModel, Arm


class Random(MABModel):
    def __init__(
            self,
            n_arms: int,
    ):
        super().__init__(n_arms)

        # Initialize internal models of arm rewards
        self.arms = [_Arm(arm_index=1) for _ in range(n_arms)]

    def select_arm(self, deltas: list[float]) -> int:
        # Save context for reward learning once reward is given
        return random.randint(0, len(self.arms) - 1)

    def update_reward(self, reward: float) -> None:
        pass

    @property
    def name(self):
        return "Linear UCB"


class _Arm(Arm):
    def __init__(self, arm_index: int):
        super().__init__(arm_index=arm_index)

    def calculate_ucb(self, x_array) -> float:
        return 0

    def update_dist(self, reward, x_array):
        pass
