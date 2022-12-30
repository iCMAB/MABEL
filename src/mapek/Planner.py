from mapek.Component import Component
from mapek.Executer import Executer
from mapek.Knowledge import Knowledge

class Planner(Component):
    def __init__(self, executer: Executer):
        self.executer = executer

    def execute(self, new_speeds: list):
        knowledge = Knowledge()
        starting_speeds = knowledge.starting_speeds

        # Speed modifier will be added to current ACV speed to get the desired speed
        speed_modifiers = list()
        for (index, new_speed) in enumerate(new_speeds):
            speed_modifiers.append(new_speed - starting_speeds[index])

        self.executer.execute(speed_modifiers)