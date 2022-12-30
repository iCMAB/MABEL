from mapek.Knowledge import Knowledge
from mapek.Analyzer import Analyzer
from mapek.Observer import Observer
from mapek.Component import Component

class Monitor(Observer, Component):
    def __init__(self, analyzer: Analyzer):
        self.analyzer = analyzer

    def update(self, distances: list, starting_speeds: list):
        # Copy info and pass to analyzer
        self.execute(distances.copy(), starting_speeds.copy())

    def execute(self, distances: list, starting_speeds: list):
        knowledge = Knowledge()
        knowledge.starting_speeds = starting_speeds

        self.analyzer.execute(distances)
        