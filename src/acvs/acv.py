from src.utils import Freezable
from src.ml_models import MABModel


class ACV(Freezable):
    """Represents an Autonomously Controlled Vehicle (ACV). Travels in one dimension.

    Attributes:
        index (int): The index of the ACV.
        location (float): The current location of the ACV.
        speed (float): The current speed of the ACV.
        distance (float): The distance between the ACV and the ACV in front of it.
        total_penalty (float): The total penalty incurred by the ACV.
        total_regret (float): The total regret of the ACV.
        baseline_penalty (float): The baseline penalty of the ACV (no MAB model in place).
        baseline_regret (float): The baseline regret of the ACV (no MAB model in place).
    """

    def __init__(
            self,
            id: int,
            location: float = 0,
            speed: float = 0,
            target_distance: float = 5,
            max_acceleration: float = 1,
            max_speed: float = 10,
    ):
        self.id = id
        self.location = location
        self.speed = speed
        self.target_distance = target_distance
        self.max_acceleration = max_acceleration
        self.max_speed = max_speed

        self.ignoring_sensor = False
        self.target_speed = None
        self.observed_distance = None
        self.distance_record = []

    def move(self):
        target_acceleration = self.target_speed - self.speed
        # Approach target speed bounded by max and min acceleration
        bounded_acceleration = max(-self.max_acceleration, min(self.max_acceleration, target_acceleration))
        self.speed += bounded_acceleration
        self.location += self.speed

    def set_distance(self, new_distance: float):
        """
        Sets the distance between the ACV and the ACV in front of it, then recomputes the predicted distance.

        Args:
            new_distance (float): The new distance between the ACV and the ACV in front of it.
        """
        self.observed_distance = new_distance

        self.distance_record.append(new_distance)
        if len(self.distance_record) > 5:
            self.distance_record.pop(0)
