from mapek.Component import Component
from mapek.Knowledge import Knowledge
from mapek.Planner import Planner
from copy import deepcopy

from config import get_config

class Analyzer(Component):
    """
    The MAPE-K loop analyzer component.

    Attributes:
        planner (Planner): The planner component of the MAPE-K loop
        distances (list): List of distances from each trailing ACV
        locations (list): List of locations of each ACV
        acvs (list): List of all ACVs
        bad_sensor (int): The index of the trailing ACV with the bad sensor reading (index of 0 will correspond to ACV1)
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
        self.bad_sensor = None

    def execute(self, acvs: list):
        """
        Calculates the new speed and penalty incurred by each trailing ACV, as well as whether or not there is a bad sensor this 
        iteration, and sends all information to the planner
        
        Args:
            acvs (list): List of all ACVs
        """

        knowledge = Knowledge()

        self.acvs = acvs
        trailing_acvs = acvs[1:]
        self.distances = [(acv.distance, knowledge.actual_distances[i]) for (i, acv) in enumerate(trailing_acvs)]
        self.locations = [acv.location for acv in acvs]

        self.handle_bad_sensor_detection()

        ideal_distance = knowledge.ideal_distance

        new_speeds = list()
        penalties = list()

        index = 0
        for (index, acv) in enumerate(trailing_acvs):
            sensor_distance = acv.distance
            actual_distance = knowledge.actual_distances[index]

            # Speed (S) = target speed (T) + (distance (D) - ideal distance (I)) → S = T + (D - I)
            new_speed = knowledge.target_speed + (sensor_distance - ideal_distance)
            actual_speed = knowledge.target_speed + (actual_distance - ideal_distance)
            
            # Predicted speed may be used in the future
            # predicted_speed = knowledge.target_speed + (predicted_distance - ideal_distance)

            # Separate penalties for the potential bad sensor reading and the ground truth
            sensor_penalty = self.calculate_penalty(sensor_distance, index)
            actual_penalty = self.calculate_penalty(actual_distance, index)

            new_speeds.append((new_speed, actual_speed))
            penalties.append((sensor_penalty, actual_penalty)) 

            index += 1

        self.planner.execute(new_speeds, penalties, self.bad_sensor, trailing_acvs)
        
    def handle_bad_sensor_detection(self):
        """Finds if there is a bad sensor reading using the chosen MAB model and updates the model's parameters"""
        
        knowledge = Knowledge()
        model = knowledge.mab_model
        self.bad_sensor = None

        trailing_acvs = self.acvs[1:]
        readings = [acv.distance for acv in trailing_acvs]        
        variations = [abs(knowledge.ideal_distance - reading) for reading in readings]

        arm = model.select_arm(variations=variations)

        penalty = self.calculate_penalty(readings[arm], arm)
        predicted_penalty = model.theta[arm]
        residual = abs(penalty - predicted_penalty)

        if residual > get_config('mab', 'residual_threshold'):
            self.bad_sensor = arm

            # New penalty with actual, unmodified distance
            penalty = self.calculate_penalty(self.distances[arm][1], arm)

        model.update(arm=arm, x=variations[arm], penalty=penalty)

    def calculate_penalty(self, distance, index) -> float:
        """
        Calculates the penalty using the formula Penalty (P) = variation (V) from desired ^2 → P = V^2, as well by predicting crashes, for 
        an ACV given distance between it and the one in front of it
        
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

        acv_index = index + 1

        # Crash penalty calculation
        for (i, acv) in enumerate(acvs):
            if (i == 0):
                acv.update(0)
                continue

            sensor_distance = acv.distance

            # Use sensor distance for all except the specified index, in which case use the distance value given as a parameter
            dist = sensor_distance if acv_index != i else distance
            
            # Speed (S) = target speed (T) + (distance (D) - ideal distance (I)) → S = T + (D - I)
            if self.bad_sensor != None and index == self.bad_sensor:
                new_speed = target_speed + (knowledge.actual_distances[index] - ideal_distance)
            else:
                new_speed = target_speed + (dist - ideal_distance)
            
            modifier = new_speed - acv.target_speed
            acv.update(modifier)

        locations = [acv.location for acv in acvs]

        crash_front = False if (acv_index == 0) else (locations[acv_index - 1] - locations[acv_index] < 0)
        crash_back = False if (acv_index >= len(locations) - 1) else (locations[acv_index] - locations[acv_index + 1] < 0)

       # We know the sensor was altered if the sensor distance and the actual distance are different
        sensor_altered = (self.distances[index][0] != self.distances[index][1])

        # A very large penalty is incurred to the ACV with the altered sensor if it crashes into another ACV 
        if ((crash_front or crash_back) and (sensor_altered)):
            penalty = get_config('mab', 'crash_penalty') 

        return penalty