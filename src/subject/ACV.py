class ACV:
    def __init__(self, index: int, start_location: float, start_speed: float):
        """
        Initializes the ACV with the given index, location, and speed.
        
        Args:
            index (int): The index of the ACV.
            start_location (float): The starting location of the ACV.
            start_speed (float): The starting speed of the ACV.
        """

        self.index = index
        self._location = start_location
        self._speed = start_speed  

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    def update(self, speed_modifier):
        """
        Updates the ACV's speed and location based on the given speed modifier.

        Args:
            speed_modifier (float): The speed modifier to apply to the ACV.
        """
        
        self.speed += speed_modifier
        self.location += self.speed