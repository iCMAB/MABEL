class Knowledge:
    __instance = None

    target_speed = None
    ideal_distance = None
    starting_speeds = None

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance

    # @property
    # def target_speed(self):
    #     return self.target_speed

    # @target_speed.setter
    # def target_speed(self, value):
    #     self.target_speed = value

    # @property
    # def ideal_distance(self):
    #     return self._ideal_distance

    # @ideal_distance.setter
    # def ideal_distance(self, value):
    #     self.ideal_distance = value

    # @property
    # def starting_speeds(self):
    #     return self.starting_speeds

    # @starting_speeds.setter
    # def starting_speeds(self, value):
    #     self.starting_speeds = value
