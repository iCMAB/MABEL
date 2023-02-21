from mapek.Component import Component
from mapek.Knowledge import Knowledge
from mapek.Planner import Planner
from copy import deepcopy
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
        self.locations = list()
        self.acvs = list()
        self.iteration = 0
        self.bad_sensor = None

    def execute(self, acvs: list):
        """
        Calculates the new speed, the potential penalties incurred, and the confidence of the distance readings for each ACV and sends them to the planner
        
        Args:
            distances (list): List of distances from the sensors for each ACV
        """

        knowledge = Knowledge()

        self.acvs = acvs
        trailing_acvs = acvs[1:]

        self.distances = [(acv.distance, knowledge.actual_distances[i]) for (i, acv) in enumerate(trailing_acvs)]
        self.locations = [acv.location for acv in acvs]

        ideal_distance = knowledge.ideal_distance

        new_speeds = list()
        penalties = list()

        # ********************LINUCB*********************

        readings = [acv.distance for acv in trailing_acvs]

        model = knowledge.model

        self.bad_sensor = None
        arm = model.select_arm()
        print("Arm value is "+str(arm))
        # print(readings[arm])
        reward = np.random.beta(1, readings[arm])
        # print(arm, readings)

        penalty = self.calculate_penalty(readings[arm], arm)
        
        # residual = abs(penalty - np.dot(model.theta[arm], readings[arm]))[0]
        
        # residual = abs(penalty - np.dot(model.theta[arm], readings[arm])[0])
        # print("Arm" + str(arm), "Residual: " + str(residual))
        # if residual > 5:
        #     self.bad_sensor = arm
        #     penalty = self.calculate_penalty(self.distances[arm][1], arm)

        model.update(arm, reward)
        self.iteration += 1

        # ************************************************

        index = 0
        for (index, acv) in enumerate(trailing_acvs):
            sensor_distance = acv.distance
            predicted_distance = acv.predicted_distance
            actual_distance = knowledge.actual_distances[index]

            # Speed (S) = target speed (T) + (distance (D) - ideal distance (I)) → S = T + (D - I)
            new_speed = knowledge.target_speed + (sensor_distance - ideal_distance)
            predicted_speed = knowledge.target_speed + (predicted_distance - ideal_distance)
            actual_speed = knowledge.target_speed + (actual_distance - ideal_distance)

            # Separate penalties for the potential bad sensor reading and the ground truth
            sensor_penalty = self.calculate_penalty(sensor_distance, index)
            actual_penalty = self.calculate_penalty(actual_distance, index)
            
            # TODO: In the future, the chosen ML model will determine the confidence value of the distance reading.
            # For now, ACVs are always fully confidenct that the distance is correct.
            # confidence = 1

            new_speeds.append((new_speed, actual_speed))
            penalties.append((sensor_penalty, actual_penalty)) 
            # confidences.append(confidence)

            index += 1

        self.planner.execute(new_speeds, penalties, self.bad_sensor, trailing_acvs)
        
    # TODO: Penalty calculation and crash detection does not take into account the predicted distance if the sensor is ignored
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
        target_speed = knowledge.target_speed
        acvs = deepcopy(self.acvs)

        # Penalty (P) = variation (V) from desired ^2 → P = V^2
        penalty = pow(distance - ideal_distance, 2)

        # Crash penalty calculation
        for (i, acv) in enumerate(acvs):
            if (i == 0):
                acv.update(0)
                continue

            sensor_distance = acv.distance

            # Use sensor distance for all except the specified index, in which case use the distance value given as a parameter
            dist = sensor_distance if index != i else distance
            
            # Speed (S) = target speed (T) + (distance (D) - ideal distance (I)) → S = T + (D - I)
            new_speed = target_speed + (dist - ideal_distance)
            modifier = new_speed - acv.target_speed

            acv.update(modifier)

        locations = [acv.location for acv in acvs]

        acv_index = index + 1

        crash_front = False if (acv_index == 0) else (locations[acv_index - 1] - locations[acv_index] < 0)
        crash_back = False if (acv_index >= len(locations) - 1) else (locations[acv_index] - locations[acv_index + 1] < 0)

        # We know the sensor was altered if the sensor distance and the actual distance are different
        sensor_altered = (self.distances[index][0] != self.distances[index][1])

        # A very large penalty is incurred to the ACV with the altered sensor if it crashes into another ACV 
        if ((crash_front or crash_back) and (sensor_altered or self.bad_sensor == index)):
            penalty = 1000000 

        return penalty