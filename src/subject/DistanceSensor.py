import pandas, time

from subject.Observable import Observable
from subject.ACV import ACV
from mapek.Knowledge import Knowledge

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
            self.print_acv_locations()
            self.update_distances()
            time.sleep(1)

    def update_distances(self):
        knowledge = Knowledge()
        distances = list()
        speeds = list()

        # Get distances between ACVs
        for (index, acv) in enumerate(self.acvs):
            if index == 0:
                knowledge.target_speed = acv.speed
                continue

            distances.append(self.acvs[index - 1].location - acv.location)
            speeds.append(acv.speed)
        
        self.notify(distances, speeds)
    
    def recieve_speed_modifications(self, speed_modifiers: list):
        for (index, acv) in enumerate(self.acvs):
            if index == 0:
                acv.update(0)
                continue

            acv.update(speed_modifiers[index - 1])
    
    def print_acv_locations(self):
        locations = list()
        
        for acv in self.acvs:
            locations.append(acv.location)

        print(locations)