from mapek.Component import Component
from mapek.Knowledge import Knowledge
from mapek.Planner import Planner
import subject

import numpy as np


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
        self.distances = list()

    def execute(self, distances: list):
        """
        Calculates the new speed, the potential penalties incurred, and the confidence of the distance readings for each ACV and sends them to the planner
        
        Args:
            distances (list): List of distances from the sensors for each ACV
        """

        self.distances = distances

        knowledge = Knowledge()
        ideal_distance = knowledge.ideal_distance
        target_speed = knowledge.target_speed

        new_speeds = list()
        penalties = list()

        # ********************LINUCB*********************

        readings = [distance[1] for distance in distances]
        # print(readings)

        model = knowledge.model

        bad_sensor = None
        arm = model.select_arm(readings)

        penalty = self.calculate_penalty(readings[arm], arm)
                
        residual = abs(penalty - np.dot(model.theta[arm], readings[arm])[0])
        # print ("Arm: ", arm, "Residual: ", residual)
        if residual > 6:
            bad_sensor = arm
            penalty = self.calculate_penalty(distances[arm][0], arm)

        # print("Bad sensor: ", bad_sensor)
        model.update(arm, readings[arm], penalty)

        #************************************************

        index = 0
        for (actual_distance, sensor_distance) in distances:
            # Speed (S) = target speed (T) + (distance (D) - ideal distance (I)) → S = T + (D - I)
            new_speed = target_speed + (sensor_distance - ideal_distance)

            # Separate penalties for the potential bad sensor reading and the ground truth
            sensor_penalty = self.calculate_penalty(sensor_distance, index)
            actual_penalty = self.calculate_penalty(actual_distance, index)
            
            # TODO: In the future, the chosen ML model will determine the confidence value of the distance reading.
            # For now, ACVs are always fully confidenct that the distance is correct.
            # confidence = 1

            new_speeds.append(new_speed)
            penalties.append((sensor_penalty, actual_penalty)) 
            # confidences.append(confidence)

            index += 1

        self.planner.execute(new_speeds, penalties, bad_sensor)
        
    def calculate_penalty(self, distance, index) -> float:
        """
        Calculates the penalty using the formula Penalty (P) = variation (V) from desired ^2 → P = V^2 for an ACV given distance between it and the one in front of it
        
        Args:
            distance (float): What the distance sensor percieves is the distance between the given ACV and the one in front of it
            index (int): The index of the ACV in the given list of ACV distances and locations (0 is ACV1, 1 is ACV2, etc.)            

        Returns:
            float: The penalty for the ACV
        """

        knowledge = Knowledge()
        ideal_distance = knowledge.ideal_distance
        starting_speeds = knowledge.starting_speeds
        locations = knowledge.locations.copy()
        target_speed = knowledge.target_speed

        locations[0] += target_speed

        # Penalty (P) = variation (V) from desired ^2 → P = V^2
        penalty = pow(distance - ideal_distance, 2)

        # Crash penalty calculation
        for i, distance_pair in enumerate(self.distances):
            sensor_distance = distance_pair[1]

            # Use sensor distance for all except the specified index, in which case use the distance value given as a parameter
            dist = sensor_distance if index != i else distance
            
            # Speed (S) = target speed (T) + (distance (D) - ideal distance (I)) → S = T + (D - I)
            new_speed = target_speed + (dist - ideal_distance)

            # Predict new ACV location given the new speed
            easing = subject.ACV_EASING
            locations[i+1] += (starting_speeds[i] + (new_speed - starting_speeds[i]) * easing)

        crash_front = False if (index == 0) else (locations[index - 1] - locations[index] < 0)
        crash_back = False if (index >= len(locations) - 1) else (locations[index] - locations[index + 1] < 0)

        # We know the sensor was altered if the sensor distance and the actual distance are different
        sensor_altered = (self.distances[index][0] != self.distances[index][1])

        # A very large penalty is incurred to the ACV with the altered sensor if it crashes into another ACV 
        if ((crash_front or crash_back) and sensor_altered):
            penalty = 1000000 

        return penalty