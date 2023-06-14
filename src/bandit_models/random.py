import random

import numpy as np

from .mab_model import MABModel


class Random(MABModel):
    def __init__(
            self,
            n_arms: int,
    ):
        super().__init__(n_arms)

    def select_arm(self, context: list[float]) -> int:
        # Save context for reward learning once reward is given
        return random.randrange(0, self.n_arms)

    def update_reward(self, reward: float) -> None:
        pass

    @property
    def name(self):
        return "Random"
