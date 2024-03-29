import subject

from config import get_config

class ACV:
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

    def __init__(self, index: int, start_location: float, start_speed: float):
        """
        Initializes the ACV with the given index, location, and speed.
        
        Args:
            index (int): The index of the ACV.
            start_location (float): The starting location of the ACV.
            start_speed (float): The starting speed of the ACV.
        """

        self.index = index
        self.location = start_location
        self.target_speed = start_speed  
        self.speed = start_speed
        
        self.distance = 0
        self.distance_record = list()
        self.predicted_distance = 0

        self.total_penalty = 0
        self.total_regret = 0
        self.baseline_penalty = 0
        self.baseline_regret = 0

    def update(self, speed_modifier, penalty=0, regret=0, baseline_penalty=0, baseline_regret=0):
        """
        Updates the ACV's speed and location based on the given speed modifier.

        Args:
            speed_modifier (float): The speed modifier to apply to the ACV.
            penalty (float): The penalty incurred in this iteration
            regret (float): The regret incurred in this iteration
            baseline_penalty (float): The baseline penalty incurred in this iteration
            baseline_regret (float): The baseline regret incurred in this iteration
        """

        self.total_penalty += penalty
        self.total_regret += regret

        self.baseline_penalty += baseline_penalty
        self.baseline_regret += baseline_regret

        max_speed = get_config('acvs', 'max_speed')
        self.target_speed += speed_modifier
        self.target_speed = max(min(self.target_speed, max_speed), -max_speed)

        easing = get_config('acvs', 'easing')
        self.speed = (self.speed + (self.target_speed - self.speed) * easing)

        self.location += self.speed

    def set_distance(self, new_distance: float):
        """
        Sets the distance between the ACV and the ACV in front of it, then recomputes the predicted distance.
        
        Args:
            new_distance (float): The new distance between the ACV and the ACV in front of it.
        """
        self.distance = new_distance

        self.distance_record.append(new_distance)
        if (len(self.distance_record) > 5):
            self.distance_record.pop(0)

        self.predicted_distance = sum(self.distance_record) / len(self.distance_record)


