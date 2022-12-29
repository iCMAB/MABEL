from mapek.Component import Component
from mapek.Knowledge import Knowledge

from subject.DistanceSensor import DistanceSensor

class Executer(Component):
    def __init__(self, sensor: DistanceSensor):
        self.sensor = sensor

    def execute(self, speed_modifiers: list):
        self.sensor.recieve_speed_modifications(speed_modifiers)