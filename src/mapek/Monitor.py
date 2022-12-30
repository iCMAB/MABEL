from mapek.Knowledge import Knowledge
from mapek.Analyzer import Analyzer
from mapek.Observer import Observer
from mapek.Component import Component

class Monitor(Observer, Component):
    """
    The MAPE-K loop monitor component.
    
    Attributes:
        analyzer (Analyzer): The analyzer component of the MAPE-K loop
    """

    def __init__(self, analyzer: Analyzer):
        """Initializes the MAPE-K loop monitor with the analyzer."""

        self.analyzer = analyzer

    def update(self, distances: list, starting_speeds: list):
        """Sends a copy of the distances and speeds to be executed on"""

        self.execute(distances.copy(), starting_speeds.copy())

    def execute(self, distances: list, starting_speeds: list):
        """
        Updates knowledge with starting speeds and sends the distances and speeds to the analyzer
        
        Args:
            distances (list): List of distances from the sensors for each relevant ACV
            starting_speeds (list): List of starting speeds for each relevant ACV
        """

        knowledge = Knowledge()
        knowledge.starting_speeds = starting_speeds

        self.analyzer.execute(distances)
        