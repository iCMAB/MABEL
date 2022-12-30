from abc import ABC, abstractmethod

class Observer(ABC):
    """Generic observer class for the observer pattern that gets notified of changes in observable"""

    @abstractmethod
    def update(index, distances: list, starting_speeds: list):
        """Generic update method for observers"""
        pass