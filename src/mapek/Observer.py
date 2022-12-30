from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(index, distances: list, starting_speeds: list):
        """Generic update method for observers"""
        pass