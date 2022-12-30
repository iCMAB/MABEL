from mapek.Component import Component

class Observable:
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

    def notify(self, distances: list, starting_speeds: list):
        """
        Notify all subscribers of changes to distances and speeds in the observable

        Args:
            distances (list): The distances between the ACV and the one in front
            starting_speeds (list): The current speeds of the ACV
        """

        for subscriber in self.subscribers:
            subscriber.update(distances, starting_speeds)