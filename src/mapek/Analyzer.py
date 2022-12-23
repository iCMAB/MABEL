import numpy

from mapek.Component import Component
from mapek.Knowledge import Knowledge
from mapek.Planner import Planner

class Analyzer(Component):
    def __init__(self, planner: Planner):
        self.planner = planner

    def execute(self, positions):
        knowledge = Knowledge()

        index = knowledge.current_index
        ideal_distance = knowledge.ideal_distance

        print(positions)

        current_position = positions.pop(index)
        current_position = numpy.asarray(current_position)
        
        distances = list()
        for position in positions:
            to_position = numpy.asarray(position)
            distance = numpy.linalg.norm(current_position - to_position, axis=0)
            distances.append(distance)

        closest_distance = min(distances)
        penalty = numpy.square(closest_distance - ideal_distance)
        knowledge.distance_to_closest = closest_distance
        knowledge.penalty = penalty

        system_will_adapt = penalty > 1
        self.planner.execute(system_will_adapt)
        
