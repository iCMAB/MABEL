import subject, itertools

class Logger:
    def __init__(self, acvs: list, iterations_to_mod: dict):
        self.acvs = acvs
        self.iterations_to_mod = iterations_to_mod
        self.column_width = 9    # Width of each column
        self.iter_col_width = 4  # Iteration count column width

        # 3 columns per ACV (distance, speed, location) minus lead ACV columns
        self.num_acv_columns = (len(acvs) - 1) * 3

    def print_acv_locations(self, iteration: int, crash_list: dict):
        """
        Prints the locations of each ACV for a given iteration.

        Args:
            iteration (int): The current iteration.
        """

        # Iteration column is 4 wide, each location/speed column is the same width. Format makes it so each ACV is divided by || and each individual column is divided by |
        spacings = ['{:>{iter}}'] + ['{:^{width}}' for _ in range(self.num_acv_columns + 2)]    # +2 for lead ACV columns
        table_template = [spacings[0] + "||" + spacings[1] + "|" + spacings[2]]     # Iter + lead ACV columns dividers
        table_template += ["||" + "|".join(spacings[3*i:3*i+3]) for i in range(1, (self.num_acv_columns // 3) + 1)]  # All other ACV columns
        table_template = "".join(table_template)

        if iteration == 0:
            self.print_table_header(table_template)

        # Get locations and speeds for each ACV
        locations = [round(acv.location, 2) for acv in self.acvs]
        speeds = [round(acv.speed, 2) for acv in self.acvs]
        distances = [round(acv.distance, 2) for acv in self.acvs]

        # Print index and alternating speed/location columns for the respective ACV (// is floor division)
        lead_acv_col = [speeds[0], locations[0]]
        trailing_acv_cols = list(itertools.chain.from_iterable([[distances[i], speeds[i], locations[i]] for i in range(1, len(self.acvs))]))
        column_aggregate = table_template.format(iteration, *lead_acv_col, *trailing_acv_cols, iter=self.iter_col_width, width=self.column_width)

        # Handle distance modification and crash flags
        flags = ""
        if (iteration in self.iterations_to_mod):
            mod_values = self.iterations_to_mod[iteration]
            flags += "ACV" + str(mod_values[0]) + " Dst x" + str(mod_values[1])

        if (crash_list != []):
            separator = " : " if flags != "" else ""
            flags += separator + "CRASH " + "".join(["(ACV" + str(crash[0]) + ", ACV" + str(crash[1]) + ")" for crash in crash_list]) 

        if (flags != ""):
            flags = "<-- " + flags 

        print(
         column_aggregate + flags, end='')
        input()

    def print_table_header(self, table_template: str):
        # Print out ideal distance and which iterations will be modified
        print("=====================================\n")
        print("• ACV Count: " + str(len(self.acvs)))
        print("• Ideal distance: " + str(subject.IDEAL_DISTANCE))
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
        print(table_template.format(*detail_headers, iter=self.iter_col_width, width=self.column_width))

        # Print divider
        print(table_template.replace(" ", "-").replace(":", ":-").replace("|", "+")
            .format(*['', '', ''] + ['' for _ in range(self.num_acv_columns)], iter=self.iter_col_width, width=self.column_width))

    def print_final_metrics(self, crashes: int):
        print("\n=====================================")
        print("\nTotal crashes: " + str(crashes))
        print ("Total penalties incurred: ", end='')
        print (*["\n• ACV" + str(acv.index) + ": " + '{0:.2f}'.format(acv.total_penalty) for acv in self.acvs])
        print()