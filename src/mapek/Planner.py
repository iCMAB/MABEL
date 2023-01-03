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

    def execute(self, new_speeds: list):
        """
        Calculates what to modify the current ACV speeds by to reach the desired speeds and sends it to the executer
        
        Args:
            new_speeds (list): List of desired speeds for each relevant ACV
        """
        knowledge = Knowledge()
        starting_speeds = knowledge.starting_speeds

        # Speed modifier will be added to current ACV speed to get the desired speed
        actual_modifiers = list()
        predicted_modifiers = list()
        for (index, new_speed) in enumerate(new_speeds):
            actual_modifiers.append(new_speed - starting_speeds[index])
            
            # Predict no change if actual modifier has a low enough confidence. May replace with something more sophisticated at some point.
            predicted_modifiers.append(0) 

        knowledge.predicted_modifiers = predicted_modifiers.copy()
        self.executer.execute(actual_modifiers)