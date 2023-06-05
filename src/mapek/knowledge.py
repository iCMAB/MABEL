class Knowledge:
    """
    The knowledge component of the MAPE-K loop.
    
    Attributes:
        target_speed (int): The target speed for all ACVs
        ideal_distance (int): The ideal distance for all ACVs
        actual_distances (list): List of unmodified distance for each trailing ACV
        mab_model (MABModel): The MAB model used to determine bad sensor readings
    """

    __instance = None

    target_speed = None
    ideal_distance = None
    actual_distances = None
    
    mab_model = None

    def __new__(cls, *args):
        """Creates a singleton instance of the Knowledge class."""
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance
