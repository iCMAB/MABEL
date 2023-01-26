from mapek.Component import Component
from mapek.Knowledge import Knowledge

from subject.ACVUpdater import ACVUpdater

class Executer(Component):
    """
    The MAPE-K loop executer component.

    Attributes:
        sensor (ACVUpdater): The distance sensor to send adaptation information back to.
    """

    def __init__(self, sensor: ACVUpdater):
        """
        Initializes the MAPE-K loop executer with the distance sensor.
        
        Args:
            sensor (ACVUpdater): The distance sensor to send adaptation information back to.
        """

        self.sensor = sensor

    def execute(self, speed_modifiers: list, penalties: list, regrets: list, acvs_ignoring_sensor: list):
        """
        Sends the speed modifiers back to the distance sensor to then be sent to the ACVs

        Args:
            speed_modifiers (list): List of speed modifiers for each ACV
            penalties (list): List of penalties for each ACV
            regrets (list): List of regrets for each ACV
            acvs_ignoring_sensor (list): List of ACVs who have ignored their distance sensor reading in favor of the predicted value. Used for visual purposes.
        """

        self.sensor.recieve_speed_modifications(speed_modifiers, penalties, regrets, acvs_ignoring_sensor)