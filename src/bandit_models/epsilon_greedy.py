import random
from collections import defaultdict
import numpy as np

from src.utils import CONFIG
from .mab_model import MABModel


class EpsilonGreedy(MABModel):
    def __init__(
            self,
            n_arms: int,
    ):
        super().__init__(n_arms)

        # Initialize internal models of arm rewards
        self.arms = [_Arm(arm_index=1) for _ in range(n_arms)]

        self.epsilon = CONFIG["models"]["epsilon_greedy"]["epsilon"]

    def select_arm(self, context: list[float]) -> int:
        return 0

    def update_reward(self, reward: float) -> None:
        self.arms[self.arm_choice].update_dist(reward=reward, x_array=self.context)

    @property
    def name(self):
        return "Linear UCB"


class _Arm:
    def __init__(self, arm_index: int):
        super().__init__(arm_index=arm_index)

        self.total_actions = 0
        self.total_rewards = 0
        self.all_rewards = []
        self.record = defaultdict(lambda: dict(actions=0, reward=0))

    def calculate_ucb(self, x_array) -> float:
        return 0.0

    def update_dist(self, reward, x_array):
        pass
