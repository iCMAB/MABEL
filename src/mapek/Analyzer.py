import numpy

from mapek.Component import Component
from mapek.Knowledge import Knowledge
from mapek.Planner import Planner

class Analyzer(Component):
    def __init__(self, planner: Planner):
        self.planner = planner

    def execute(self, distances: list):
        knowledge = Knowledge()
        target_speed = knowledge.target_speed
        ideal_distance = knowledge.ideal_distance

        speeds = list()
        for distance in distances:
            current_Speed = target_speed + (distance - ideal_distance)
            speeds.append(current_Speed)

        self.planner.execute(speeds)
        
