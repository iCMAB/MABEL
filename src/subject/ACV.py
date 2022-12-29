class ACV:
    def __init__(self, index: int, start_location: float, start_speed: float, ideal_distance: float):
        self.index = index
        self.location = start_location
        self.speed = start_speed
        self.ideal_distance = ideal_distance

        self.speed_history = list()
        self.distance_history = list()
        
        self.speed_history.append(start_speed)

    def update(self, speed):
        self.speed = speed
        self.location += self.speed

        self.speed_history.append(self.speed)