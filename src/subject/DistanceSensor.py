import pandas, time, subject, random

from subject.Observable import Observable
from subject.ACV import ACV
from mapek.Knowledge import Knowledge

class DistanceSensor(Observable):
    def __init__(self):
        super().__init__()
        self.acvs = list()
        self.iteration = 0
        self.iterations_to_mod = self.calculate_mod_iterations()

    def calculate_mod_iterations(self) -> dict:
        num_iterations = subject.ITERATIONS
        mod_percent = subject.PERCENT_MODIFIED
        num_modded = round(num_iterations * mod_percent) # Floors the decimal value for all positive numbers

        mod_iterations = random.sample(range(0, num_iterations), num_modded)
        iteration_mod_pair = {
            iteration:
            round(random.uniform(subject.MOD_RANGE[0], subject.MOD_RANGE[1]), 2)
            for iteration in mod_iterations
        }

        iteration_mod_pair = dict(sorted(iteration_mod_pair.items()))
        return iteration_mod_pair

    def read_data(self):
        data = pandas.read_csv('data/acv_start.csv')

        # Initialize ACVs
        for index, row in data.iterrows():
            self.acvs.append(ACV(int(row['acv_index']), float(row['location']), float(row['speed'])))

        self.run_update_loop()

    def run_update_loop(self):
        for i in range(subject.ITERATIONS):
            self.iteration = i
            self.print_acv_locations(i)
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

            distance = self.mod_distance(self.acvs[index - 1].location - acv.location)

            distances.append(distance)
            speeds.append(acv.speed)
        
        # Send distance and speed data for all ACVs except lead to MAPE-K loop
        self.notify(distances, speeds)
    
    def mod_distance(self, distance) -> float:
        modded_distance = distance
        if self.iteration in self.iterations_to_mod.keys():
            modded_distance = distance * self.iterations_to_mod[self.iteration]
        
        return modded_distance

    def recieve_speed_modifications(self, speed_modifiers: list):
        for (index, acv) in enumerate(self.acvs):
            # Don't modify speed of lead ACV
            if index == 0:
                acv.update(0)
                continue

            acv.update(speed_modifiers[index - 1])
    
    def print_acv_locations(self, index):
        # 2 columns per ACV (location, speed)
        acv_columns = len(self.acvs) * 2

        # index column is 4 wide, each location/speed column is 8 wide
        template = " | ".join(['{:>4}'] + ['{:^8}' for _ in range(acv_columns)])

        if index == 0:
            # Print out which iterations will be modified
            print("=====================================")
            print("Ideal distance: " + str(subject.IDEAL_DISTANCE))
            print("Modifying distance in iterations: \n", *["> " + str(iteration) + " (x" + str(value) + ")\n" for iteration, value in self.iterations_to_mod.items()])

            # Header for ACV index (ACV1, ACV2, etc.)
            acv_headers = [''] + ['ACV' + str(acv.index + 1) for acv in self.acvs]

            # Each ACV column is 19 wide to account for 2 8-wide columns plus the 3-character divider
            acv_template = " | ".join(['{:>4}'] + ['{:^19}' for _ in range(len(self.acvs))])
            print(acv_template.format(*acv_headers))

            # Headers for iteration index and alternating speed/location columns
            detail_headers = ['Iter'] + [('Speed' if i % 2 == 0 else 'Location') for i in range(acv_columns)]
            print(template.format(*detail_headers))

            # Print divider
            print(template.replace(" ", "-").replace(":", ":-").replace("|", "+").format(*[''] + ['' for _ in range(acv_columns)]))

        # Get locations and speeds for each ACV
        locations = list()
        speeds = list()
        for acv in self.acvs:
            locations.append(round(acv.location, 2))
            speeds.append(round(acv.speed, 2))

        # Print index and alternating speed/location columns for the respective ACV (// is floor division)
        column = template.format(index, *[speeds[i // 2] if i % 2 == 0 else locations[i // 2] for i in range(acv_columns)]) 
        if (index in self.iterations_to_mod):
            column += " <--- DISTANCE MODIFIED (x" + str(self.iterations_to_mod[index]) + ")"

        print(column)