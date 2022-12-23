import pandas, time

from subject.Observable import Observable

class PositionSensor(Observable):
    def __init__(self):
        super().__init__()
        self.positions = [(0,0)] * 5

    def read_data(self):
        data = pandas.read_csv('data/acv_readings.csv')
        for index, row in data.iterrows():
            self.positions[int(row['acv_index'])] = (row['x'], row['y'])
            print(self.positions)
            time.sleep(0.5)

    def notify_num(self):
        self.notify(42)
        