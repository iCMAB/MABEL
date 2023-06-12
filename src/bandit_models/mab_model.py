from abc import ABC, abstractmethod


class MABModel(ABC):
    def __init__(
            self,
            n_arms: int,
    ):
        self.n_arms = n_arms
        self.context = None
        self.arms: list[Arm]
        self.arm_choice: int = 0

    @abstractmethod
    def select_arm(self, deltas: list[float]) -> int:
        """
        Implementations will use this method to select an arm based on the information given to the model

        Args:
            deltas: The distance deltas between the observed distances and the target distances for each ACV

        Returns: The index of the arm to ignore the sensor value or -1 to not ignore any sensor
        """

    @abstractmethod
    def update_reward(self, reward: float) -> None:
        pass

    @property
    @abstractmethod
    def name(self):
        pass

class Arm(ABC):
    def __init__(self, arm_index: int):
        # Track arm index
        self.arm_index = arm_index

    @abstractmethod
    def calculate_ucb(self, x_array) -> float:
        pass

    @abstractmethod
    def update_dist(self, reward, x_array):
        pass

