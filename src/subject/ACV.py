import subject

class ACV:
    """Represents an Autonomously Controlled Vehicle (ACV). Travels in one dimension.
    
    Attributes:
        index (int): The index of the ACV.
        location (float): The current location of the ACV.
        speed (float): The current speed of the ACV.
        distance (float): The distance between the ACV and the ACV in front of it.
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
        self.speed = start_speed  
        self.distance = 0

    def update(self, speed_modifier):
        """
        Updates the ACV's speed and location based on the given speed modifier.

        Args:
            speed_modifier (float): The speed modifier to apply to the ACV.
        """

        self.speed += speed_modifier
        self.speed = max(min(self.speed, subject.MAX_SPEED), -subject.MAX_SPEED)
        
        self.location += self.speed