from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(index, positions):
        pass