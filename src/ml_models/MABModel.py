from abc import ABC, abstractmethod

class MABModel(ABC):
    
    @abstractmethod
    def select_arm(**kwargs):
        """
        Implementations will use this method to select an arm based on the information given to the model
        
        Args:
            **kwargs: The information given to the model used to select an arm. May include the sensor readings
        """
        pass

    @abstractmethod
    def update(**kwargs):
        """
        Implementations will use this method to update the model based on the reading and the penalty incurred
        
        Args:
            **kwargs: The information given to the model to update itself. May include the arm that was selected, the reading of the sensor whose arm was selected, and the penalty incurred by the selected arm
        """
        pass