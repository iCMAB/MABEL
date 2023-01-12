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
        penalties = list()
        regrets = list()
        for (actual_distance, modded_distance) in distances:
            current_Speed = target_speed + (modded_distance - ideal_distance)
            speeds.append(current_Speed)

            # Penalty (P) = variation (V) from desired ^2 → P = V^2
            modded_penalty = pow(modded_distance - ideal_distance, 2)
            actual_penalty = pow(actual_distance - ideal_distance, 2)

            # Regret (R) = modded penalty (Pm) - actual penalty (Pa) → R = Pm - Pa
            regret = modded_penalty - actual_penalty
            
            regrets.append(regret)
            penalties.append(modded_penalty) 
            confidences.append(1)   # In the future, the ML model will determine the confidence value

        knowledge.confidences = confidences.copy()
        knowledge.penalties = penalties.copy()
        knowledge.regrets = regrets.copy()

        self.planner.execute(speeds)
        
