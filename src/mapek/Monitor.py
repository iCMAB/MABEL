from mapek.Knowledge import Knowledge
from mapek.Analyzer import Analyzer
from mapek.Observer import Observer
from mapek.Component import Component

from copy import deepcopy

class Monitor(Observer, Component):
    """
    The MAPE-K loop monitor component.
    
    Attributes:
        analyzer (Analyzer): The analyzer component of the MAPE-K loop
    """

    def __init__(self, analyzer: Analyzer):
        """
        Initializes the MAPE-K loop monitor with the analyzer.
        
        Args:
            analyzer (Analyzer): The analyzer component of the MAPE-K loop
        """

        self.analyzer = analyzer

    def update(self, acvs: list, actual_distances: list):
        """
        Sends a copy of the distances and speeds to be executed on
        
        Args:
            acvs (list): List of all ACVs
            actual_distances (list): List of unmodified distance for each trailing ACV
        """

        acvs_copy = deepcopy(acvs)
        self.execute(acvs_copy, actual_distances.copy())

    def execute(self, acvs: list, actual_distances: list):
        """
        Updates knowledge with speeds and sends the distances and speeds to the analyzer
        
        Args:
            acvs (list): List of all ACVs
            actual_distances (list): List of unmodified distance for each trailing ACV
        """

        knowledge = Knowledge()
        knowledge.actual_distances = actual_distances

        self.analyzer.execute(acvs)
        