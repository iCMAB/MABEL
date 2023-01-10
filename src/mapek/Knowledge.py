class Knowledge:
    """
    The knowledge component of the MAPE-K loop.
    
    Attributes:
        target_speed (int): The target speed for all ACVs
        ideal_distance (int): The ideal distance for all ACVs
        starting_speeds (list): List of starting speeds for each relevant ACV (not lead ACV)
        confidences (list): List of how confident the model is in the calculated (actual) speed modifier
        predicted_modifiers (list): List of predicted speed modifiers for each relevant ACV (not lead ACV)
        penalties (list): List of distance-based penalties for each relevant ACV (not lead ACV)
    """

    __instance = None

    target_speed = None
    ideal_distance = None
    starting_speeds = None
    confidences = list()
    predicted_modifiers = list()
    penalties = list()

    def __new__(cls, *args):
        """Creates a singleton instance of the Knowledge class."""
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance
