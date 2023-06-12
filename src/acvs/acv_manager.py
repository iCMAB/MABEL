import pandas, random, math

from .acv import ACV
from .logger import LOGGER
from src.utils import CONFIG
from src.bandit_models.linear_ucb import LinearUCB as MABModel


class ACVManager:
    """
    Initializes and controls the ACVs

    Attributes:
        acvs (dict): Mapping of ACV id"s to ACV objects
        frame_num (int): The current frame number of the simulation
        frames_to_mod (dict): A dictionary of iterations to modify and the amount to modify them by
        total_crashes (int): The total number of crashes that have occurred
    """

    def __init__(self, model: MABModel):
        """Initialize the ACVUpdater class."""
        self.model = model

        self.acvs: list[ACV] = acvs_from_file("data/acv_start.csv")

        self.frame_num = 0

        self.acv_distance_deltas: list[int] = [0] * len(self.acvs)
        self.ignored_sensors = []

    def run_simulation(self):
        LOGGER.print_sim_header(self.model.name, self.acvs)

        for i in range(CONFIG["simulation"]["training_iterations"]):
            self.run_frame(frame_num=i, training=True)

        for i in range(CONFIG["simulation"]["iterations"]):
            self.run_frame(frame_num=i + CONFIG["simulation"]["training_iterations"], training=False)

    def run_frame(self, frame_num: int, training: bool = False):
        # The ACVs would set their own sensors in the real world
        failed_sensors = self.set_sensors(training)

        self.monitor()
        self.analyze()
        self.plan()
        # Log behavior before actually moving the ACVs
        LOGGER.print_sim_frame(frame_num, self.acvs, failed_sensors, self.ignored_sensors)
        self.execute()

        self.check_collisions()

    def set_sensors(self, training: bool = False) -> list[int]:
        """
        Sets the sensor values for ACVs with a chance of failure

        Args:
            training: A boolean flag to disable sensor failures during the training stage

        Returns: A list of (id, failure ratio) tuples describing all sensor failures
        """
        failed_sensors = []
        for i, acv in enumerate(self.acvs):
            distance = self.get_distance_to_next_acv(i)
            if (not training
                and not acv == self.acvs[-1]
                and random.random() < CONFIG["simulation"]["sensor_failure_rate"]
            ):
                failure_ratio = random.uniform(*CONFIG["simulation"]["sensor_failure_range"])
                distance = distance * failure_ratio
                failed_sensors.append(acv.id)
            acv.set_distance(distance)
        return failed_sensors

    def check_collisions(self):
        acv_list = self.acvs
        crashes = []
        for acv, next_acv in zip(acv_list, acv_list[1:]):
            if acv.location > next_acv.location:
                crashes.append(acv)
        return crashes

    def monitor(self):
        """Get observed distances from every ACV"""
        if self.model.context:
            # Don't update reward if no decisions have been made yet
            reward = 0
            for i, acv in enumerate(self.acvs):
                if acv != self.acvs[-1]:
                    # Since we want to avoid sub-optimal behavior, reward is negative (regret)
                    reward -= math.pow(acv.target_distance - self.get_distance_to_next_acv(i), 2)
            self.model.update_reward(reward)

        for i, acv in enumerate(self.acvs):
            if acv.observed_distance:
                self.acv_distance_deltas[i] = acv.observed_distance - acv.target_distance
            else:
                self.acv_distance_deltas[i] = 0

    def analyze(self):
        """

        Returns:

        """
        arm_selection = self.model.select_arm(self.acv_distance_deltas) - 1
        if arm_selection >= 0:
            self.ignored_sensors = [arm_selection]
        else:
            self.ignored_sensors = []

    def plan(self):
        for i, acv in enumerate(self.acvs):
            if i in self.ignored_sensors:
                acv.ignoring_sensor = True
                acv.target_speed = 5
            else:
                acv.ignoring_sensor = False
                acv.target_speed = acv.observed_distance or (acv.max_speed / 2)

    def execute(self):
        for acv in self.acvs:
            acv.move()

    def get_distance_to_next_acv(self, index):
        if index + 1 < len(self.acvs):
            return self.acvs[index + 1].location - self.acvs[index].location
        else:
            return None


def acvs_from_file(acv_file_path: str) -> list[ACV]:
    """Reads the starting data from the CSV file, initializes the ACVs, and starts the update loop."""
    data = pandas.read_csv(acv_file_path)

    acv_init_values = []
    for i, row in data.iterrows():
        acv_init_values.append((row["start_location"], row["start_speed"]))

    acvs = []
    for i, acv_values in enumerate(sorted(acv_init_values, key=lambda x: x[0])):
        acvs.append(ACV(
            id=i,
            location=float(acv_values[0]),
            speed=float(acv_values[1]),
            target_distance=CONFIG["acvs"]["target_distance"],
            max_acceleration=CONFIG["acvs"]["max_acceleration"],
            max_speed=CONFIG["acvs"]["max_speed"],
        ))

    if len(acvs) < 2:
        raise Exception("Please initialize 2 or more ACVs with unique indexes from the CSV file.")
    if len(acvs) != CONFIG["acvs"]["num_acvs"]:
        print(f"WARNING: Number of ACVs specified in {acv_file_path} overrides config file.")

    return acvs

    # def calculate_mod_iterations(self) -> dict:
    #     """
    #     Calculates the iterations that will be modified and the amount to modify them by.
    #
    #     Returns:
    #         dict: A dictionary of iterations to modify as keys and the ACV to modify as well as amount to modify them by as the values.
    #     """
    #
    #     num_iterations = get_config("simulation", "iterations")
    #     mod_percent = get_config("simulation", "percent_modified")
    #     training_iters = get_config("simulation", "training_iterations")
    #     mod_range = get_config("simulation", "mod_range")
    #
    #     num_modded = round(num_iterations * mod_percent)  # Floors the decimal value for all positive numbers
    #
    #     mod_iterations = random.sample(range(training_iters + 1, num_iterations), num_modded)
    #     iteration_mod_pair = {
    #         iteration:
    #             (
    #                 random.randint(1, get_config("acvs", "num_acvs") - 1),  # ACV index
    #                 round(random.uniform(mod_range[0], mod_range[1]), 2)  # Mod amount
    #             )
    #         for iteration in mod_iterations
    #     }
    #
    #     iteration_mod_pair = dict(sorted(iteration_mod_pair.items()))
    #     return iteration_mod_pair
    #
    # def run_update_loop(self):
    #     """Runs the update loop for the distance sensor."""
    #
    #     logger = Logger(self.acvs, self.iterations_to_mod)
    #
    #     for i in range(get_config("simulation", "iterations") + 1):
    #         self.iteration = i
    #
    #         # Only update after first iteration so iteration 0 displays the starting values
    #         if (i > 0):
    #             self.update_distances()
    #
    #         logger.acvs_ignoring_sensor = self.acvs_ignoring_sensor
    #         logger.print_acv_locations(i, self.detect_crashes())
    #
    #     logger.print_final_metrics(self.total_crashes)
    #
    # def update_distances(self):
    #     """Updates the distances between the ACVs and sends the data to the MAPE-K loop to determine speed adaptation."""
    #
    #     knowledge = Knowledge()
    #     actual_distances = list()
    #     speeds = list()
    #     locations = list()
    #
    #     # Get distances between ACVs
    #     for (index, acv) in enumerate(self.acvs):
    #         # Collect locations of all ACVs, including ACV0
    #         locations.append(acv.location)
    #
    #         if index == 0:
    #             knowledge.target_speed = acv.speed
    #             continue
    #
    #         actual_distance = self.acvs[index - 1].location - acv.location
    #
    #         # Represents bad sensor reading modification
    #         modded_distance = self.mod_distance(actual_distance, index)
    #
    #         acv.set_distance(modded_distance)
    #
    #         actual_distances.append(actual_distance)
    #         speeds.append(acv.speed)
    #
    #     # Send distance and speed data for all ACVs except lead to MAPE-K loop
    #     self.notify(self.acvs, actual_distances)
    #
    # def mod_distance(self, distance, index) -> float:
    #     """
    #     Determines if a distance should be modified based on the current iteration and returns the modified distance.
    #     Does nothing if the distance should not be modified.
    #
    #     Args:
    #         distance (float): The distance to be modified.
    #         index (int): The index of the ACV that the distance is for.
    #
    #     Returns:
    #         float: The modified distance.
    #     """
    #
    #     modded_distance = distance
    #     if self.iteration in self.iterations_to_mod.keys() and self.iterations_to_mod[self.iteration][0] == index:
    #         modded_distance = distance * self.iterations_to_mod[self.iteration][1]
    #
    #     return modded_distance
    #
    # def recieve_speed_modifications(self, speed_modifiers: list, penalties: list, regrets: list,
    #                                 baseline_penalties: list, baseline_regrets: list, acvs_ignoring_sensor: list):
    #     """
    #     Updates each ACV with a speed modification, penalty, and regret
    #
    #     Args:
    #         speed_modifiers (list): A list of speed modifiers to apply to each ACV.
    #         penalties (list): A list of penalties for each ACV in this iteration.
    #         regrets (list): A list of regrets for each ACV in this iteration.
    #         baseline_penalties (list): A list of baseline penalties for each ACV in this iteration.
    #         baseline_regrets (list): A list of baseline regrets for each ACV in this iteration.
    #         acvs_ignoring_sensor (list): List of ACVs who have ignored their distance sensor reading in favor of the predicted value. Used for visual purposes.
    #     """
    #
    #     self.acvs_ignoring_sensor = acvs_ignoring_sensor.copy()
    #
    #     for (index, acv) in enumerate(self.acvs):
    #         # Don"t modify speed of lead ACV - speed is always constant
    #         if index == 0:
    #             acv.update(0)
    #             continue
    #
    #         i = index - 1
    #         acv.update(speed_modifiers[i], penalties[i], regrets[i], baseline_penalties[i], baseline_regrets[i])
    #
    # def detect_crashes(self) -> list:
    #     """
    #     Checks if an ACV has crashed into another ACV.
    #
    #     Returns:
    #         list(): A list of tuples containing the two crashed ACVs.
    #     """
    #
    #     crash_list = list()
    #     for (index, acv) in enumerate(self.acvs):
    #         if index == 0:
    #             continue
    #
    #         if acv.location >= self.acvs[index - 1].location:
    #             crash_list.append((index - 1, index))
    #
    #     self.total_crashes += len(crash_list)
    #     return crash_list
