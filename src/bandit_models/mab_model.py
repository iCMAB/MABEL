from abc import ABC, abstractmethod
import numpy as np


class MABModel(ABC):
    def __init__(
            self,
            n_arms: int,
    ):
        self.n_arms = n_arms

        self.context: np.ndarray = None
        self.arm_choice: int = None

    @abstractmethod
    def select_arm(self, context: list[float]) -> int:
        """
        Implementations will use this method to select an arm based on the information given to the model

        Args:
            context: The distance deltas between the observed distances and the target distances for each ACV

        Returns: The index of the arm to ignore the sensor value or -1 to not ignore any sensor
        """

    @abstractmethod
    def update_reward(self, reward: float) -> None:
        pass

    @property
    @abstractmethod
    def name(self):
        pass
