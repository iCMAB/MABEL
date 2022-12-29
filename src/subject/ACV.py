class ACV:
    def __init__(self, index: int, start_location: float, start_speed: float, ideal_distance: float):
        self.index = index
        self._location = start_location
        self._speed = start_speed
        self.ideal_distance = ideal_distance

        self.speed_history = list()
        self.distance_history = list()
        
        self.speed_history.append(start_speed)

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
        self.speed += speed_modifier
        self.location += self.speed

        self.speed_history.append(self.speed)