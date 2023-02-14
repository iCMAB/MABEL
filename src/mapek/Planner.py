from mapek.Component import Component
from mapek.Executer import Executer
from mapek.Knowledge import Knowledge

class Planner(Component):
    """The MAPE-K loop planner component.
    
    Attributes:
        executer (Executer): The executer component of the MAPE-K loop
    """

    def __init__(self, executer: Executer):
        """Initializes the MAPE-K loop planner with the executer."""

        self.executer = executer

    def execute(self, new_speeds: list, penalties: list, bad_sensor: int, trailing_acvs: list):
        """
        Calculates what to modify the current ACV speeds by based on the confidence measurement and sends it along with the penaly and regret incurred to the executer
        
        Args:
            new_speeds (list): List of desired speeds for each ACV
            penalties (list): List of tuples containing the penalty for the distance sensor value and actual distance vlaue respectively for each ACV. 
            confidences (list): List of confidence values for each ACV measuring the confidence in this iteration's distance sensor value 
        """

        knowledge = Knowledge()
        starting_speeds = knowledge.starting_speeds

        confidence_threshold = 0.5  # TODO: Decide how to handle this value

        # Speed modifier will be added to current ACV speed to get the desired speed
        speed_modifiers = list()

        chosen_penalties = list()
        regrets = list()

        # Simply the penalties and regrets from distance sensor readings. Baseline values used to show what would have happened if no distance sensor correction has been performed. 
        baseline_penalties = list()
        baseline_regrets = list()
        
        # ACVs who have ignored their distance sensor reading in favor of the predicted value. Used for visual purposes.
        acvs_ignoring_sensor = list()    

        for (index, acv) in enumerate(trailing_acvs):
            sensor_penalty = penalties[index][0]
            actual_penalty = penalties[index][1]

            normal_modifier = new_speeds[index] - acv.target_speed
            predicted_modifier = knowledge.target_speed - acv.target_speed  # Defaults to target speed if actual modifier has a low enough confidence. May replace with something more sophisticated at some point.
           
            modifier_to_add = normal_modifier
            penalty_to_incur = sensor_penalty

            # If confidence is low enough, go with the predicted value instead of the value from the distance sensor
            # if confidences[index] < confidence_threshold:
            if bad_sensor != None and index == bad_sensor:
                modifier_to_add = predicted_modifier
                penalty_to_incur = actual_penalty
                acvs_ignoring_sensor.append(index + 1)   # ACV0 not counted, so add 1 to index
            
            # Regret (R) = modded penalty (Pm) - actual penalty (Pa) → R = Pm - Pa
            regret = penalty_to_incur - actual_penalty
            baseline_regret = sensor_penalty - actual_penalty

            speed_modifiers.append(modifier_to_add)
            chosen_penalties.append(penalty_to_incur)
            regrets.append(regret)

            baseline_penalties.append(sensor_penalty)
            baseline_regrets.append(baseline_regret)

        self.executer.execute(speed_modifiers, chosen_penalties, regrets, baseline_penalties, baseline_regrets, acvs_ignoring_sensor)