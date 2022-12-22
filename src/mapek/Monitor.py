from mapek.Observer import Observer
from mapek.Component import Component

class Monitor(Observer):
    def __init__(self):
        pass

    def update(self, num):
        print(num)