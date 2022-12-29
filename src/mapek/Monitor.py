from mapek.Knowledge import Knowledge
from mapek.Analyzer import Analyzer
from mapek.Observer import Observer
from mapek.Component import Component

class Monitor(Observer, Component):
    def __init__(self, analyzer: Analyzer):
        self.analyzer = analyzer

    def update(self, index, distances):
        self.execute(index, distances.copy())

    def execute(self, index, distances):
        knowledge = Knowledge()
        knowledge.current_index = index

        print(distances)

        # self.analyzer.execute(distance)
        