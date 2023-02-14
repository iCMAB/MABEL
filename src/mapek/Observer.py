from abc import ABC, abstractmethod

class Observer(ABC):
    """Generic observer class for the observer pattern that gets notified of changes in observable. Used by the Monitor component of the MAPE-K loop."""

    @abstractmethod
    def update(acvs: list, actual_distances: list):
        """
        Generic update method for observers to be overridden.
        
        Args:
            distances (list): List of distances from the sensors for each relevant ACV
            starting_speeds (list): List of starting speeds for each relevant ACV
        """
        pass