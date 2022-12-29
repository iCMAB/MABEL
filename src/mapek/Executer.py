from mapek.Component import Component
from mapek.Knowledge import Knowledge

from subject.DistanceSensor import DistanceSensor

class Executer(Component):
    def __init__(self, sensor: DistanceSensor):
        self.sensor = sensor

    def execute(self, plan):
        knowledge = Knowledge()

        index = knowledge.current_index
        distance_to_closest = knowledge.distance_to_closest
        penalty = knowledge.penalty

        self.sensor.receive_decision(index, distance_to_closest, penalty, plan)