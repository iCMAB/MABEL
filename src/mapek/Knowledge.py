class Knowledge:
    __instance = None

    target_speed = None
    ideal_distance = None
    starting_speeds = None

    def __new__(cls, *args):
        """Creates a singleton instance of the Knowledge class."""
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance
