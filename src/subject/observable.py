from ..mapek import Component
# TODO: Import coupling

class Observable:
    """
    An observable class for the observer pattern that can be subscribed to and notified of changes
    
    Attributes:
        subscribers (set): A set of all subscribers to the observable
    """

    def __init__(self):
        """Initialize the observable with an empty set of subscribers"""
        self.subscribers = set()

    def register(self, component: Component):
        """
        Register a component to be notified when the observable changes
        
        Args:
            component (Component): The component to register
        """

        self.subscribers.add(component)

    def deregister(self, component: Component):
        """
        Deregister a component from being notified when the observable changes
        
        Args:
            component (Component): The component to deregister
        """

        self.subscribers.remove(component)

    def notify(self, acvs: list, actual_distances: list):
        """
        Notify all subscribers of changes to distances and speeds in the observable

        Args:
            distances (list): The distances between the ACV and the one in front
            speeds (list): The current speeds of the ACV
            locations (list): The current locations of the ACV
        """

        for subscriber in self.subscribers:
            subscriber.update(acvs, actual_distances)