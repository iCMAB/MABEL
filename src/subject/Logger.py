import subject, itertools, colorama

from tabulate import tabulate

class Logger:
    """
    Used to log a visual representation of the ACV simulation to the console
    
    Attributes:
        acvs (list): List of ACVs in the simulation
        iterations_to_mod (dict): A dictionary of iterations to modify and the amount to modify them by
        column_width (int): The width of each column
        iter_col_width (int): The width of the first column used as an interation tally
        num_acv_columns (int): The number of columns used to represent each ACV (minus the lead ACV)
        table_template (str): The template used to create a row in the table
    """

    MODIFIED_DST_COLOR = colorama.Back.YELLOW
    IGNORED_DST_COLOR = colorama.Back.GREEN
    CRASH_COLOR = colorama.Back.RED
    COLOR_RESET = colorama.Back.RESET

    def __init__(self, acvs: list, iterations_to_mod: dict):
        """
        Initialize the Logger class.
        
        Args:
            acvs (list): List of ACVs in the simulation
            iterations_to_mod (dict): A dictionary of iterations to modify and the amount to modify them by
        """
        colorama.init()
        
        self.acvs = acvs
        self.iterations_to_mod = iterations_to_mod
        self.column_width = 9    # Width of each column
        self.iter_col_width = 4  # Iteration count column width

        # 3 columns per ACV (distance, speed, location) minus lead ACV columns
        self.num_acv_columns = (len(acvs) - 1) * 3
        self.row_template = self.get_row_template()

        self.acvs_ignoring_sensor = list()

    def get_row_template(self) -> str:
        """
        Creates the string template for a row in the outputted table
        
        Returns:
            str: The template for a row in the table
        """

        # Iteration column is 4 wide, each location/speed column is the same width. Format makes it so each ACV is divided by || and each individual column is divided by |
        spacings = ['{:>{iter}}'] + ['{:^{width}}' for _ in range(self.num_acv_columns + 2)]    # +2 for lead ACV columns
        
        table_template = [spacings[0] + "||" + spacings[1] + "|" + spacings[2]]     # Iter + lead ACV columns dividers
        table_template += ["||" + "|".join(spacings[3*i:3*i+3]) for i in range(1, (self.num_acv_columns // 3) + 1)]  # All other ACV columns
        table_template = "".join(table_template)
        
        return table_template

    def find_iteration_flags(self, iteration: int, crash_list: dict, locations: list, distances: list) -> str:
        """
        Handles the logic necessary for distance modification and crash "flags," such as table cell coloring and text descriptors
        
        Args:
            iteration (int): The current iteration
            crash_list (dict): A list of crashes that occurred in the current iteration
            locations (list): A list of locations for each ACV
            distances (list): A list of distances for each ACV
        
        Returns:
            str: A string containing the flags for the current iteration to be displayed to the left of the table
        """

        flags = ""

        # Handle distance modification
        if (iteration in self.iterations_to_mod):
            mod_values = self.iterations_to_mod[iteration]  # mod_values is a tuple -> (acv_index, distance_to_modify)

            # Distance is colored green if the ACV is ignoring the distance sensor value, yellow otherwise
            color = Logger.IGNORED_DST_COLOR if mod_values[0] in self.acvs_ignoring_sensor else Logger.MODIFIED_DST_COLOR
            distances[mod_values[0]] = self.modify_cell_color(distances[mod_values[0]], color)

            mod_values = self.iterations_to_mod[iteration]
            flags += "ACV" + str(mod_values[0]) + " Dst x" + str(mod_values[1])

        # Handle crashes
        if (crash_list != []):
            for crash in crash_list:
                locations[crash[0]] = self.modify_cell_color(locations[crash[0]], Logger.CRASH_COLOR)
                locations[crash[1]] = self.modify_cell_color(locations[crash[1]], Logger.CRASH_COLOR)

            separator = " : " if flags != "" else ""
            flags += separator + "CRASH " + "".join(["(ACV" + str(crash[0]) + ", ACV" + str(crash[1]) + ")" for crash in crash_list]) 

        if (flags != ""):
            flags = " <-- " + flags 

        return flags

    def modify_cell_color(self, value, color) -> str:
        """
        Modifies the color of a cell in the table
        
        Args:
            value (str): The value to be modified
            color (any): The color to change the cell to
        
        Returns:
            str: The colored cell
        """
        return str(color + '{:^{width}}'.format(value, width=self.column_width) + Logger.COLOR_RESET)

    def print_acv_locations(self, iteration: int, crash_list: dict):
        """
        Prints the locations of each ACV for a given iteration.

        Args:
            iteration (int): The current iteration.
            crash_list (dict): A list of crashes that occurred in the current iteration.
        """

        if iteration == 0:
            self.print_table_header()

        # Get locations and speeds for each ACV
        locations = [round(acv.location, 2) for acv in self.acvs]
        speeds = [round(acv.speed, 2) for acv in self.acvs]
        distances = [round(acv.distance, 2) for acv in self.acvs]

        # Get flags before conputing the column aggregate so that cell highlighting can be applied
        flags = self.find_iteration_flags(iteration, crash_list, locations, distances)

        # Print index and alternating speed/location columns for the respective ACV (// is floor division)
        lead_acv_col = [speeds[0], locations[0]]
        trailing_acv_cols = list(itertools.chain.from_iterable([[distances[i], speeds[i], locations[i]] for i in range(1, len(self.acvs))]))
        column_aggregate = self.row_template.format(iteration, *lead_acv_col, *trailing_acv_cols, iter=self.iter_col_width, width=self.column_width)

        print(
         column_aggregate + flags, end='')
        input()

    def print_table_header(self):
        """Prints the table header"""

        # Print out ideal distance and which iterations will be modified
        print("=====================================\n")
        print("• ACV Count: " + str(len(self.acvs)))
        print("• Ideal distance: " + str(subject.IDEAL_DISTANCE))
        print("• Total Iterations: " + str(subject.ITERATIONS))
        print("• Distance modification iterations: ", 
            *["\n   > " + str(iteration) + " (ACV" + str(value[0]) + ", " + str(value[1]) + "x)" for iteration, value in self.iterations_to_mod.items()])

        print("\nPress enter to continue...")
        input()

        # Header for ACV index (ACV1, ACV2, etc.)
        acv_headers = [''] + ['ACV' + str(acv.index) for acv in self.acvs]

        # Lead ACV column is 19 wide (2 6-wide columns + 1 1-character divider)
        # All other ACV columns are 30 wide (3 5-wide columns + 2 1-character dividers)
        acv_template = "||".join(['{:>{iter}}', '{:^{lead_acv}}'] + ['{:^{acv}}' for _ in range(len(self.acvs) - 1)])
        print(acv_template.format(*acv_headers, iter=self.iter_col_width, lead_acv=(self.column_width * 2 + 1), acv=(self.column_width * 3 + 2)))

        # Headers for iteration index and alternating speed/location columns
        detail_headers = ['Iter', 'Spd', 'Loc'] + [('Dst' if i % 3 == 0 else ('Spd' if i % 3 == 1 else 'Loc')) for i in range(self.num_acv_columns)]
        print(self.row_template.format(*detail_headers, iter=self.iter_col_width, width=self.column_width))

        # Print divider
        print(self.row_template.replace(" ", "-").replace(":", ":-").replace("|", "+")
            .format(*['', '', ''] + ['' for _ in range(self.num_acv_columns)], iter=self.iter_col_width, width=self.column_width))

    def print_final_metrics(self, crashes: int):
        """
        Prints the final metrics for the simulation
        
        Args:
            crashes (int): The number of crashes that occurred during the simulation
        """

        def round_two_decimals(value: float) -> str:
            return '{0:.2f}'.format(value)

        print("\n=====================================\n")

        table=[
            [
                acv.index, 
                round_two_decimals(acv.total_penalty), 
                round_two_decimals(acv.total_regret),
                round_two_decimals(acv.baseline_penalty), 
                round_two_decimals(acv.baseline_regret)
            ] for acv in self.acvs]
        headers=["ACV Index", "Penalty", "Regret", "Baseline Penalty", "Baseline Regret"]
        print(tabulate(table, headers, tablefmt="fancy_grid", disable_numparse=True))
        
        # Bullet point metrics
        avg_penalty = round_two_decimals(sum([acv.total_penalty for acv in self.acvs]) / len(self.acvs))
        avg_baseline_penalty = round_two_decimals(sum([acv.baseline_penalty for acv in self.acvs]) / len(self.acvs))
        total_regret = round_two_decimals(sum([acv.total_regret for acv in self.acvs]))
        total_baseline_regret = round_two_decimals(sum([acv.baseline_regret for acv in self.acvs]))

        penalty_improvement = round_two_decimals((float(avg_baseline_penalty) - float(avg_penalty)) / float(avg_baseline_penalty) * 100)
        regret_improvement = round_two_decimals((float(total_baseline_regret) - float(total_regret)) / float(total_baseline_regret) * 100)

        print("\nLinUCB Metrics:")
        print("• Total crashes: " + str(crashes))
        
        print("• Average penalty:\t\tAverage baseline penalty:")
        print("    " + avg_penalty + "\t\t\t  " + avg_baseline_penalty)
        print("• Total regret:\t\t\tTotal baseline regret:")
        print("    "  + total_regret + "\t\t\t  " + total_baseline_regret)
        
        print("• Improvement in avg penalty:\t" + str(penalty_improvement) + "%")
        print("• Improvement in total regret:\t" + str(regret_improvement) + "%")

        print()