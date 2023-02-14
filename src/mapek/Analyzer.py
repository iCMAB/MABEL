from mapek.Component import Component
from mapek.Knowledge import Knowledge
from mapek.Planner import Planner
import subject

import numpy as np
import math

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
        self.locations = list()
        self.trailing_acvs = list()
        self.iteration = 0

    def execute(self, acvs: list):
        """
        Calculates the new speed, the potential penalties incurred, and the confidence of the distance readings for each ACV and sends them to the planner
        
        Args:
            distances (list): List of distances from the sensors for each ACV
        """

        knowledge = Knowledge()

        trailing_acvs = acvs[1:]
        self.trailing_acvs = trailing_acvs

        self.distances = [(acv.distance, knowledge.actual_distances[i]) for (i, acv) in enumerate(trailing_acvs)]
        self.locations = [acv.location for acv in acvs]

        ideal_distance = knowledge.ideal_distance

        new_speeds = list()
        penalties = list()

        # ********************LINUCB*********************

        readings = [acv.distance for acv in trailing_acvs]

        model = knowledge.model

        bad_sensor = None
        arm = model.select_arm(readings)

        penalty = self.calculate_penalty(readings[arm], arm)
                
        residual = abs(penalty - np.dot(model.theta[arm], readings[arm])[0])
        # print("Arm" + str(arm), "Residual: " + str(residual))
        if residual > 6:
            bad_sensor = arm
            penalty = self.calculate_penalty(self.distances[arm][1], arm)

        model.update(arm, readings[arm], penalty)
        self.iteration += 1

        # ************************************************

        index = 0
        for (index, acv) in enumerate(trailing_acvs):
            sensor_distance = acv.distance
            actual_distance = knowledge.actual_distances[index]

            # Speed (S) = target speed (T) + (distance (D) - ideal distance (I)) → S = T + (D - I)
            new_speed = knowledge.target_speed + (sensor_distance - ideal_distance)

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

        self.planner.execute(new_speeds, penalties, bad_sensor, trailing_acvs)
        
    # TODO: Move into the subject folder and send penalty back to model after MAPE-K runs
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
        locations = self.locations.copy()
        target_speed = knowledge.target_speed
        trailing_acvs = self.trailing_acvs

        locations[0] += target_speed

        # Penalty (P) = variation (V) from desired ^2 → P = V^2
        penalty = pow(distance - ideal_distance, 2)

        # Crash penalty calculation
        for (i, acv) in enumerate(trailing_acvs):
            sensor_distance = acv.distance

            # Use sensor distance for all except the specified index, in which case use the distance value given as a parameter
            dist = sensor_distance if index != i else distance
            
            # Speed (S) = target speed (T) + (distance (D) - ideal distance (I)) → S = T + (D - I)
            s = target_speed + (dist - ideal_distance)
            modifier = s - acv.target_speed
            new_speed = acv.target_speed + modifier

            # Predict new ACV location given the new speed
            easing = subject.ACV_EASING
            speed = (starting_speeds[i] + (new_speed - starting_speeds[i]) * easing)
            
            locations[i+1] += speed

        crash_front = False if (index == 0) else (locations[index - 1] - locations[index] < 0)
        crash_back = False if (index >= len(locations) - 1) else (locations[index] - locations[index + 1] < 0)

        # We know the sensor was altered if the sensor distance and the actual distance are different
        sensor_altered = (self.distances[index][0] != self.distances[index][1])

        # A very large penalty is incurred to the ACV with the altered sensor if it crashes into another ACV 
        if ((crash_front or crash_back) and sensor_altered):
            penalty = 1000000 

        return penalty