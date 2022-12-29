import pandas, time

from subject.Observable import Observable
from subject.ACV import ACV

class DistanceSensor(Observable):
    def __init__(self):
        super().__init__()
        self.acvs = list()

    def read_data(self):
        data = pandas.read_csv('data/acv_start.csv')

        # Initialize ACVs
        for index, row in data.iterrows():
            self.acvs.append(ACV(int(row['acv_index']), float(row['location']), float(row['speed']), float(row['ideal_distance'])))

        self.run_update_loop()

    def run_update_loop(self):
        while True:
            self.update_distances()
            time.sleep(1)

    def update_distances(self):
        distances = [0] * (len(self.acvs) - 1) # Num ACVs minus the starting one, which won't change

        # Get distances between ACVs
        for (index, acv) in enumerate(self.acvs):
            if index == 0:
                continue

            distances[index - 1] = self.acvs[index - 1].location - acv.location
        
        self.notify(index, distances)
    
    def update_acv_speeds(self, index, speed):
        pass