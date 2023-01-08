from mapek.Component import Component
from mapek.Knowledge import Knowledge
from mapek.Planner import Planner

class Analyzer(Component):
    """
    The MAPE-K loop analyzer component.

    Attributes:
        planner (Planner): The planner component of the MAPE-K loop
    """

    def __init__(self, planner: Planner):
        """Initializes the MAPE-K loop analyzer with the planner."""

        self.planner = planner

    def execute(self, distances: list):
        """
        Calculates the desired speed for each ACV and sends it to the planner
        
        Args:
            distances (list): List of distances from the sensors for each relevant ACV
        """

        knowledge = Knowledge()
        target_speed = knowledge.target_speed
        ideal_distance = knowledge.ideal_distance

        speeds = list()
        confidences = list()
        for distance in distances:
            current_Speed = target_speed + (distance - ideal_distance)
            speeds.append(current_Speed)

            confidences.append(1)   # In the future, the ML model will determine the confidence value

        knowledge.confidences = confidences.copy()
        self.planner.execute(speeds)
        
