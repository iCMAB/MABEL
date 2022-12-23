from mapek.Knowledge import Knowledge
from mapek.Analyzer import Analyzer
from mapek.Observer import Observer
from mapek.Component import Component

class Monitor(Observer, Component):
    def __init__(self, analyzer: Analyzer):
        self.analyzer = analyzer

    def update(self, index, positions):
        self.execute(index, positions.copy())

    def execute(self, index, positions):
        knowledge = Knowledge()
        knowledge.current_index = index

        self.analyzer.execute(positions)
        