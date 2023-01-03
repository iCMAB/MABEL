from mapek.Component import Component
from mapek.Knowledge import Knowledge

from subject.DistanceSensor import DistanceSensor

class Executer(Component):
    """
    The MAPE-K loop executer component.

    Attributes:
        sensor (DistanceSensor): The distance sensor to send adaptation information back to.
    """

    def __init__(self, sensor: DistanceSensor):
        """Initializes the MAPE-K loop executer with the distance sensor."""

        self.sensor = sensor

    def execute(self, speed_modifiers: list):
        """
        Sends the speed modifiers back to the distance sensor to then be sent to the ACVs

        Args:
            speed_modifiers (list): List of speed modifiers for each relevant ACV
        """

        knowledge = Knowledge()
        confidences = knowledge.confidences
        predicted_modifiers = knowledge.predicted_modifiers

        self.sensor.recieve_speed_modifications(speed_modifiers, confidences, predicted_modifiers)