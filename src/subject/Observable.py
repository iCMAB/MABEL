from mapek.Component import Component

class Observable:
    def __init__(self):
        self.subscribers = set()

    def register(self, component: Component):
        self.subscribers.add(component)

    def deregister(self, component: Component):
        self.subscribers.remove(component)

    def notify(self, index: int, positions: list):
        for subscriber in self.subscribers:
            subscriber.update(index, positions)