from mapek.Component import Component
from mapek.Executer import Executer
from mapek.Knowledge import Knowledge

class Planner(Component):
    def __init__(self, executer: Executer):
        self.executer = executer

    def execute(self, system_will_adapt):
        knowledge = Knowledge()

        distance_to_closest = knowledge.distance_to_closest
        ideal_distance = knowledge.ideal_distance

        plan = "Do nothing"
        if system_will_adapt:
            if distance_to_closest < ideal_distance:
                plan = "Slow down"
            elif distance_to_closest > ideal_distance:
                plan = "Speed up"

        self.executer.execute(plan)