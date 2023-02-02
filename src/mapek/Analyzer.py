from mapek.Component import Component
from mapek.Knowledge import Knowledge
from mapek.Planner import Planner

import numpy as np
from ml_models.linearUCB import LinearUCB

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
        Calculates the new speed, the potential penalties incurred, and the confidence of the distance readings for each ACV and sends them to the planner
        
        Args:
            distances (list): List of distances from the sensors for each ACV
        """

        knowledge = Knowledge()
        ideal_distance = knowledge.ideal_distance
        target_speed = knowledge.target_speed

        new_speeds = list()
        confidences = list()
        penalties = list()

        # ********************LINUCB*********************
        readings = [distance[1] for distance in distances]

        d = 1
        alpha = 0.1
        model = LinearUCB(d, alpha)

        bad_sensors = []
        arm = model.select_arm(readings)
        penalty = self.calculate_penalty(readings[arm])
        
        # residual = abs(penalty - np.dot(model.theta[arm], readings[arm]))[0]
        
        residual = abs(penalty - np.dot(model.theta[arm], readings[arm])[0])
        print("Arm", arm, "  Residual:", model.theta[arm][0])
        
        if residual > 5:
            bad_sensors.append(arm)
        model.update(arm, readings[arm], penalty)
            
        print("Bad sensors:", bad_sensors)

        #************************************************

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