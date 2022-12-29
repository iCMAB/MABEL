from mapek.Component import Component

class Observable:
    def __init__(self):
        self.subscribers = set()

    def register(self, component: Component):
        self.subscribers.add(component)

    def deregister(self, component: Component):
        self.subscribers.remove(component)

    def notify(self, distances: list, starting_speeds: list):
        for subscriber in self.subscribers:
            subscriber.update(distances, starting_speeds)