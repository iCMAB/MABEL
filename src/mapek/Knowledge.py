class Knowledge:
    __instance = None

    ideal_distance = None
    current_index = None
    current_distance_to_closest = None
    current_penalty = None

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance

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

    @property
    def penalty(self):
        return self._penalty

    @penalty.setter
    def penalty(self, value):
        self._penalty = value
