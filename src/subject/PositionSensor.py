from subject.Observable import Observable

class PositionSensor(Observable):
    def notify_num(self):
        self.notify(42)
        