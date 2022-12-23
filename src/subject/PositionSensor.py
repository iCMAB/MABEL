import pandas, time

from subject.Observable import Observable

class PositionSensor(Observable):
    def __init__(self):
        super().__init__()
        self.positions = [(0,0)] * 5

    def read_data(self):
        data = pandas.read_csv('data/acv_readings.csv')
        for index, row in data.iterrows():
            acv_index = int(row['acv_index'])
            self.positions[acv_index] = (row['x'], row['y'])
            self.notify(acv_index, self.positions)

            time.sleep(0.5)

    def notify_num(self):
        self.notify(42)
        