class Knowledge:
    __instance = None
    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance

    def __init__(self, ideal_distance):
        self.ideal_distance = ideal_distance
        self.current_index = 0
        self.distance_to_closest = None

    @property
    def ideal_distance(self):
        return self._ideal_distance

    @ideal_distance.setter
    def ideal_distance(self, value):
        self._ideal_distance = value

    @property
    def current_index(self):
        return self._current_index

    @current_index.setter
    def current_index(self, value):
        self._current_index = value

    @property
    def distance_to_closest(self):
        return self._distance_to_closest

    @distance_to_closest.setter
    def distance_to_closest(self, value):
        self._distance_to_closest = value

    def printit(self):
        print(self.ideal_distance)
        print(self.current_index)
        print(self.distance_to_closest)
        print()
