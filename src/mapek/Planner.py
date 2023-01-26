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

    def execute(self, new_speeds: list, penalties: list, confidences: list):
        """
        Calculates what to modify the current ACV speeds by to reach the desired speeds and sends it to the executer
        
        Args:
            new_speeds (list): List of desired speeds for each relevant ACV
        """

        knowledge = Knowledge()
        starting_speeds = knowledge.starting_speeds

        confidence_threshold = 0.5  # TODO: Decide how to handle this value

        # Speed modifier will be added to current ACV speed to get the desired speed
        speed_modifiers = list()

        chosen_penalties = list()
        regrets = list()

        for (index, new_speed) in enumerate(new_speeds):
            sensor_penalty = penalties[index][0]
            actual_penalty = penalties[index][1]

            normal_modifier = new_speed - starting_speeds[index]
            predicted_modifier = 0  # Predict no change if actual modifier has a low enough confidence. May replace with something more sophisticated at some point.

            modifier_to_add = normal_modifier
            penalty_to_incur = sensor_penalty

            # If confidence is low enough, go with the predicted value instead of the value from the distance sensor
            if confidences[index] < confidence_threshold:
                modifier_to_add = predicted_modifier
                penalty_to_incur = actual_penalty
            
            # Regret (R) = modded penalty (Pm) - actual penalty (Pa) → R = Pm - Pa
            regret = penalty_to_incur - actual_penalty

            speed_modifiers.append(modifier_to_add)
            chosen_penalties.append(penalty_to_incur)
            regrets.append(regret)

        self.executer.execute(speed_modifiers, chosen_penalties, regrets)