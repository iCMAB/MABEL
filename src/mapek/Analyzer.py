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
        """
        Initializes the MAPE-K loop analyzer with the planner.
        
        Args:
            planner (Planner): The planner component of the MAPE-K loop
        """

        self.planner = planner

    def execute(self, distances: list):
        """
        Calculates the desired speed for each ACV and sends it to the planner
        
        Args:
            distances (list): List of distances from the sensors for each relevant ACV
        """

        knowledge = Knowledge()
        ideal_distance = knowledge.ideal_distance
        target_speed = knowledge.target_speed

        speeds = list()
        confidences = list()
        penalties = list()
        regrets = list()

        for (actual_distance, modded_distance) in distances:
            # Speed (S) = target speed (T) + (distance (D) - ideal distance (I)) → S = T + (D - I)
            current_Speed = target_speed + (modded_distance - ideal_distance)

            modded_penalty = self.calculate_penalty(modded_distance)
            actual_penalty = self.calculate_penalty(actual_distance)

            # Regret (R) = modded penalty (Pm) - actual penalty (Pa) → R = Pm - Pa
            regret = modded_penalty - actual_penalty
            
            speeds.append(current_Speed)
            regrets.append(regret)
            penalties.append(modded_penalty) 
            confidences.append(1)   # In the future, the chosen ML model will determine the confidence value

        knowledge.confidences = confidences.copy()
        knowledge.penalties = penalties.copy()
        knowledge.regrets = regrets.copy()

        self.planner.execute(speeds)
        
    def calculate_penalty(self, distance) -> float:
        """
        Calculates the penalty using the formula Penalty (P) = variation (V) from desired ^2 → P = V^2 for an ACV given distance between it and the one in front of it
        
        Args:
            distance (float): The distance between the given ACV and the one in front of it
            
        Returns:
            float: The penalty for the ACV
        """

        knowledge = Knowledge()
        ideal_distance = knowledge.ideal_distance
        return pow(distance - ideal_distance, 2)