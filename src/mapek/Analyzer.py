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

        new_speeds = list()
        confidences = list()
        penalties = list()

        for (actual_distance, sensor_distance) in distances:
            # Speed (S) = target speed (T) + (distance (D) - ideal distance (I)) → S = T + (D - I)
            new_speed = target_speed + (sensor_distance - ideal_distance)

            # Separate penalties for the potential bad sensor reading and the ground truth
            sensor_penalty = self.calculate_penalty(sensor_distance)
            actual_penalty = self.calculate_penalty(actual_distance)
            
            # TODO: In the future, the chosen ML model will determine the confidence value of the distance reading.
            # For now, ACVs are always fully confidenct that the distance is correct.
            confidence = 1

            new_speeds.append(new_speed)
            penalties.append((sensor_penalty, actual_penalty)) 
            confidences.append(confidence)

        self.planner.execute(new_speeds, penalties, confidences)
        
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

        # Penalty (P) = variation (V) from desired ^2 → P = V^2
        penalty = pow(distance - ideal_distance, 2)

        # A very large penalty is also incurred if the vehicles collide
        if (distance <= 0):
            penalty = 1000000 
        
        return penalty