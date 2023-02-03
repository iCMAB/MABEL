import pandas, subject, random

from subject.Observable import Observable
from subject.ACV import ACV
from subject.Logger import Logger
from mapek.Knowledge import Knowledge

class ACVUpdater(Observable):
    """
    Represents the distance sensor of an ACV. Serves as the intermediary between the ACVs and the speed adaptation MAPE-K loop
    
    Attributes:
        acvs (list): List of ACVs that the distance sensor is monitoring
        iteration (int): The current iteration of the simulation
        iterations_to_mod (dict): A dictionary of iterations to modify and the amount to modify them by
        total_crashes (int): The total number of crashes that have occurred
        acvs_ignoring_sensor (list): List of ACVs who have ignored their distance sensor reading in favor of the predicted value for the current iteration. Used for visual purposes.
    """

    def __init__(self):
        """Initialize the ACVUpdater class."""

        super().__init__()
        self.acvs = list()
        self.iteration = 0
        self.iterations_to_mod = dict()
        self.total_crashes = 0
        self.acvs_ignoring_sensor = list()

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

        logger = Logger(self.acvs, self.iterations_to_mod)

        for i in range(subject.ITERATIONS + 1):
            self.iteration = i

            # Only update after first iteration so iteration 0 displays the starting values
            if (i > 0):
                self.update_distances()
            
            logger.acvs_ignoring_sensor = self.acvs_ignoring_sensor
            logger.print_acv_locations(i, self.detect_crashes())

        logger.print_final_metrics(self.total_crashes)

    def update_distances(self):
        """Updates the distances between the ACVs and sends the data to the MAPE-K loop to determine speed adaptation."""

        knowledge = Knowledge()
        distances = list()
        speeds = list()
        locations = list()

        # Get distances between ACVs
        for (index, acv) in enumerate(self.acvs):
            # Collect locations of all ACVs, including ACV0
            locations.append(acv.location)

            if index == 0:
                knowledge.target_speed = acv.speed
                continue

            actual_distance = self.acvs[index - 1].location - acv.location

            # Represents bad sensor reading modification
            modded_distance = self.mod_distance(actual_distance, index) 
            
            # The predicted distance, which will be used if the sensor reading is ignored, is the last known distance reading from the ACV
            # predicted_distance = acv.distance
            # print(predicted_distance)
            
            acv.distance = modded_distance

            distances.append((actual_distance, modded_distance))
            speeds.append(acv.speed)
            
        
        # Send distance and speed data for all ACVs except lead to MAPE-K loop
        self.notify(distances, speeds, locations)
    
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

    def recieve_speed_modifications(self, speed_modifiers: list, penalties: list, regrets: list, baseline_penalties: list, baseline_regrets: list, acvs_ignoring_sensor: list):
        """
        Updates each ACV with a speed modification, penalty, and regret
        
        Args:
            speed_modifiers (list): A list of speed modifiers to apply to each ACV.
            penalties (list): A list of penalties for each ACV in this iteration.
            regrets (list): A list of regrets for each ACV in this iteration.
            baseline_penalties (list): A list of baseline penalties for each ACV in this iteration.
            baseline_regrets (list): A list of baseline regrets for each ACV in this iteration.
            acvs_ignoring_sensor (list): List of ACVs who have ignored their distance sensor reading in favor of the predicted value. Used for visual purposes.
        """

        self.acvs_ignoring_sensor = acvs_ignoring_sensor.copy()

        for (index, acv) in enumerate(self.acvs):
            # Don't modify speed of lead ACV - speed is always constant
            if index == 0:
                acv.update(0, 0, 0, 0, 0)
                continue

            i = index - 1
            acv.update(speed_modifiers[i], penalties[i], regrets[i], baseline_penalties[i], baseline_regrets[i])

    def detect_crashes(self) -> list:
        """
        Checks if an ACV has crashed into another ACV.

        Returns:
            list(): A list of tuples containing the two crashed ACVs.
        """

        crash_list = list()
        for (index, acv) in enumerate(self.acvs):
            if index == 0:
                continue

            if acv.location >= self.acvs[index - 1].location:
                crash_list.append((index - 1, index))
        
        self.total_crashes += len(crash_list)
        return crash_list

