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
        Calculates what to modify the current ACV speeds by and sends the modifications, penalties and regrets incurred, baseline penalties/regrets, and the ACV being ignored to the executer
        
        Args:
            new_speeds (list): List of desired speeds for each ACV
            penalties (list): List of tuples containing the penalty for the distance sensor value and actual distance vlaue respectively for each ACV. 
            bad_sensor (int): The index of the trailing ACV with the bad sensor reading (index of 0 will correspond to ACV1)
            trailing_acvs (list): List of all trailing ACVs (ACV1 and beyond)
        """

        # Speed modifier will be added to current ACV speed to get the desired speed
        speed_modifiers = list()

        chosen_penalties = list()
        regrets = list()

        # Simply the penalties and regrets from distance sensor readings. Baseline values used to show what would have happened if no distance sensor correction has been performed. 
        # Used in analytics calculation at the end of the simulation
        baseline_penalties = list()
        baseline_regrets = list()
        
        # ACVs who have ignored their distance sensor reading in favor of the predicted value. Used for visual purposes.
        acvs_ignoring_sensor = list()    

        for (index, acv) in enumerate(trailing_acvs):
            sensor_penalty = penalties[index][0]
            ground_truth_penalty = penalties[index][1]

            # "new_speeds" is how fast the ACVs SHOULD go. Subtracting the target speed gives us the modifier to add to the current speed to get the desired speed
            normal_modifier = new_speeds[index][0] - acv.target_speed
            ground_truth_modifier = new_speeds[index][1] - acv.target_speed
           
            modifier_to_add = normal_modifier
            penalty_to_incur = sensor_penalty

            # If a bad sensor has been detected, ignore the sensor reading and use the ground truth value instead
            # Ground truth value acts as a "predicted" distance value for our sake
            if bad_sensor != None and index == bad_sensor:
                modifier_to_add = ground_truth_modifier
                penalty_to_incur = ground_truth_penalty
                acvs_ignoring_sensor.append(index + 1)   # ACV0 not counted, so add 1 to index
            
            # Regret (R) = modded penalty (Pm) - actual penalty (Pa) → R = Pm - Pa
            regret = penalty_to_incur - ground_truth_penalty
            baseline_regret = sensor_penalty - ground_truth_penalty

            speed_modifiers.append(modifier_to_add)
            chosen_penalties.append(penalty_to_incur)
            regrets.append(regret)

            baseline_penalties.append(sensor_penalty)
            baseline_regrets.append(baseline_regret)

        self.executer.execute(speed_modifiers, chosen_penalties, regrets, baseline_penalties, baseline_regrets, acvs_ignoring_sensor)