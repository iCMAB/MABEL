from abc import ABC, abstractmethod

class MABModel(ABC):
    
    @abstractmethod
    def select_arm(**kwargs):
        """
        Implementations will use this method to select an arm based on the information given to the model
        
        Args:
            **kwargs: The information given to the model. May include the sensor readings
        """
        pass

    @abstractmethod
    def update(arm, x, penalty):
        """
        Implementations will use this method to update the model based on the reading and the penalty incurred
        
        Args:
            arm (int): The arm that was selected
            x (list): The reading of the sensor whose arm was selected
            penalty (float): The penalty incurred by the selected arm
        """
        pass