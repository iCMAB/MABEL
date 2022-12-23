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

            time.sleep(1)

    def receive_decision(self, index, distance_to_closest, penalty, decision):
        print('ACV Index: ' + str(index))
        print('Distance to closest ACV: ' + "{0:.2f}".format(distance_to_closest))
        print('Penalty: ' + "{0:.2f}".format(penalty))
        print('Decision received: ' + str(decision))
        print()
        