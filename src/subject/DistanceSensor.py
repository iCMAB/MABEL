import pandas, subject, random, itertools

from subject.Observable import Observable
from subject.ACV import ACV
from mapek.Knowledge import Knowledge

class DistanceSensor(Observable):
    """
    Represents the distance sensor of an ACV. Serves as the intermediary between the ACVs and the speed adaptation MAPE-K loop
    
    Attributes:
        acvs (list): List of ACVs that the distance sensor is monitoring
        iteration (int): The current iteration of the simulation
        iterations_to_mod (dict): A dictionary of iterations to modify and the amount to modify them by
    """

    def __init__(self):
        """Initialize the DistanceSensor class."""
        super().__init__()
        self.acvs = list()
        self.iteration = 0
        self.iterations_to_mod = dict()

    def calculate_mod_iterations(self) -> dict:
        """
        Calculates the iterations that will be modified and the amount to modify them by.
        
        Returns:
            dict: A dictionary of iterations to modify as keys and the ACV to modify as well as amount to modify them by as the values.
        """

        num_iterations = subject.ITERATIONS
        mod_percent = subject.PERCENT_MODIFIED
        num_modded = round(num_iterations * mod_percent) # Floors the decimal value for all positive numbers

        mod_iterations = random.sample(range(0, num_iterations), num_modded)
        iteration_mod_pair = {
            iteration:
            (
                random.randint(1, len(self.acvs) - 1), # ACV index
                round(random.uniform(subject.MOD_RANGE[0], subject.MOD_RANGE[1]), 2) # Mod amount
            )
            for iteration in mod_iterations
        }

        iteration_mod_pair = dict(sorted(iteration_mod_pair.items()))
        return iteration_mod_pair

    def read_data(self):
        """Reads the starting data from the CSV file, initializes the ACVs, and starts the update loop."""

        data = pandas.read_csv('data/acv_start.csv')

        # Initialize ACVs
        for index, row in data.iterrows():
            self.acvs.append(ACV(index, float(row['start_location']), float(row['start_speed'])))

        if (len(self.acvs) <= 1):
            raise Exception('Please initialize 2 or more ACVs with unique indexes from the CSV file.')

        self.iterations_to_mod = self.calculate_mod_iterations()
        self.run_update_loop()

    def run_update_loop(self):
        """Runs the update loop for the distance sensor."""

        for i in range(subject.ITERATIONS + 1):
            self.iteration = i

            # Only update after first iteration so iteration 0 displays the starting values
            if (i > 0):
                self.update_distances()
            
            self.print_acv_locations(i)

    def update_distances(self):
        """Updates the distances between the ACVs and sends the data to the MAPE-K loop to determine speed adaptation."""

        knowledge = Knowledge()
        distances = list()
        speeds = list()

        # Get distances between ACVs
        for (index, acv) in enumerate(self.acvs):
            if index == 0:
                knowledge.target_speed = acv.speed
                continue

            distance = self.mod_distance(self.acvs[index - 1].location - acv.location, index)
            acv.distance = distance

            distances.append(distance)
            speeds.append(acv.speed)
        
        # Send distance and speed data for all ACVs except lead to MAPE-K loop
        self.notify(distances, speeds)
    
    def mod_distance(self, distance, index) -> float:
        """
        Determines if a distance should be modified based on the current iteration and returns the modified distance.
        Does nothing if the distance should not be modified.

        Args:
            distance (float): The distance to be modified.
            index (int): The index of the ACV that the distance is for.

        Returns:
            float: The modified distance.
        """

        modded_distance = distance
        if self.iteration in self.iterations_to_mod.keys() and self.iterations_to_mod[self.iteration][0] == index:
            modded_distance = distance * self.iterations_to_mod[self.iteration][1]
        
        return modded_distance

    def recieve_speed_modifications(self, actual_modifiers: list, confidences: list, predicted_modifiers: list):
        """
        Updates each ACV with speed modifications
        
        Args:
            speed_modifiers (list): A list of speed modifiers to apply to each ACV.
        """

        confidence_threshold = 0.5
        for (index, acv) in enumerate(self.acvs):
            # Don't modify speed of lead ACV
            if index == 0:
                acv.update(0)
                continue

            i = index - 1
            modify_val = actual_modifiers[i]
            if (confidences[i] < confidence_threshold):
                modify_val = predicted_modifiers[i]

            acv.update(modify_val)

    def detect_crashes(self):
        """
        Checks if an ACV has crashed into another ACV.

        Returns:
            list(): A list of tuples containing the two crashed ACVs.
        """

        crash_list = list()
        for (index, acv) in enumerate(self.acvs):
            if index == 0:
                continue

            if acv.location > self.acvs[index - 1].location:
                crash_list.append((index - 1, index))
        
        return crash_list

    def print_acv_locations(self, iteration):
        """
        Prints the locations of each ACV.

        Args:
            iteration (int): The current iteration.
        """

        column_width = 9    # Width of each column
        iter_col_width = 4  # Iteration count column width

        # 3 columns per ACV (distance, speed, location) and only 2 columns for lead ACV (speed, location)
        acv_columns = (len(self.acvs) - 1) * 3

        # Iteration column is 4 wide, each location/speed column is 8 wide. Format makes it so each ACV is divided by || and each individual column is divided by |
        spacings = ['{:>{iter}}', '{:^{width}}', '{:^{width}}'] + ['{:^{width}}' for _ in range(acv_columns)]
        template = [spacings[0] + "||" + spacings[1] + "|" + spacings[2]]     # Iter + lead ACV columns
        template += ["||" + "|".join(spacings[3*i:3*i+3]) for i in range(1, (acv_columns // 3) + 1)]  # All other ACV columns
        template = "".join(template)

        if iteration == 0:
            # Print out ideal distance and which iterations will be modified
            print("=====================================\n")
            print("• ACV Count: " + str(len(self.acvs)))
            print("• Ideal distance: " + str(subject.IDEAL_DISTANCE))
            print("• Distance modification iterations: ", *["\n   > " + str(iteration) + " (ACV" + str(value[0]) + ", " + str(value[1]) + "x)" for iteration, value in self.iterations_to_mod.items()])

            print("\nPress enter to continue...", end='')
            input()
            print()

            # Header for ACV index (ACV1, ACV2, etc.)
            acv_headers = [''] + ['ACV' + str(acv.index) for acv in self.acvs]

            # Lead ACV column is 19 wide (2 6-wide columns + 1 1-character divider)
            # All other ACV columns are 30 wide (3 5-wide columns + 2 1-character dividers)
            acv_template = "||".join(['{:>{iter}}', '{:^{lead_acv}}'] + ['{:^{acv}}' for _ in range(len(self.acvs) - 1)])
            print(acv_template.format(*acv_headers, iter=iter_col_width, lead_acv=(column_width * 2 + 1), acv=(column_width * 3 + 2)))

            # Headers for iteration index and alternating speed/location columns
            detail_headers = ['Iter', 'Spd', 'Loc'] + [('Dst' if i % 3 == 0 else ('Spd' if i % 3 == 1 else 'Loc')) for i in range(acv_columns)]
            print(template.format(*detail_headers, iter=iter_col_width, width=column_width))

            # Print divider
            print(template.replace(" ", "-").replace(":", ":-").replace("|", "+").format(*['', '', ''] + ['' for _ in range(acv_columns)], iter=iter_col_width, width=column_width))

        # Get locations and speeds for each ACV
        locations = [round(acv.location, 2) for acv in self.acvs]
        speeds = [round(acv.speed, 2) for acv in self.acvs]
        distances = [round(acv.distance, 2) for acv in self.acvs]
        crash_list = self.detect_crashes()

        # Print index and alternating speed/location columns for the respective ACV (// is floor division)
        lead_acv_col = [speeds[0], locations[0]]
        trailing_acv_cols = list(itertools.chain.from_iterable([[distances[i], speeds[i], locations[i]] for i in range(1, len(self.acvs))]))
        column_aggregate = template.format(iteration, *lead_acv_col, *trailing_acv_cols, iter=iter_col_width, width=column_width)

        # Handle distance modification and crash flags
        flags = ""
        if (iteration in self.iterations_to_mod):
            mod_values = self.iterations_to_mod[iteration]
            flags += "DISTANCE MODIFICATION (ACV" + str(mod_values[0]) + ", " + str(mod_values[1]) + "x)"

        if (crash_list != []):
            separator = " : " if flags != "" else ""
            flags += separator + "CRASH " + "".join(["(ACV" + str(crash[0]) + " + ACV" + str(crash[1]) + ")" for crash in crash_list]) 

        if (flags != ""):
            flags = "\n*** ITERATION " + str(iteration) + " FLAGS: " + flags 

        print(
         column_aggregate + flags, end='')
        input()