from .acv import ACV
from src.utils import CONFIG
from colorama import Back

class Logger:
    def __init__(self):
        self.column_width = 9  # Width of each column
        self.iter_col_width = 4  # Iteration count column width
        self.row_template = None

    def print_sim_header(self, model_name: str, acvs: list[ACV]):
        # Print out ideal distance and which iterations will be modified
        print(CONFIG["logging"]["major_divider"])

        print(f"• MAB Model: {model_name}")
        print(f"• ACV Count: {len(acvs)}")
        print(f"• Ideal Distance: {CONFIG['acvs']['target_distance']}")
        print(f"• Total Iterations: {CONFIG['simulation']['iterations']}")
        input("\nPress enter to continue...")

        # Header for ACV index (ACV1, ACV2, etc.)
        acv_headers = [''] + ['ACV' + str(acv.id) for acv in acvs]

        print(
            " " * self.iter_col_width + "||" +
            "||".join(len(acvs) * [
                "|".join([
                    "Loc".center(self.column_width, " "),
                    "Dis".center(self.column_width, " "),
                    "Spd".center(self.column_width, " "),
                ])
            ])
        )

        print(
            "-" * self.iter_col_width + "++" +
            "++".join(len(acvs) * [
                "+".join(3 * [
                    "-" * self.column_width
                ])
            ])
        )

    def print_sim_frame(self, frame_num: int, acvs: list[ACV], failed_sensors: list[int], ignored_sensors: list[int]):
        print(str(frame_num).rjust(self.iter_col_width), end="")
        for i, acv in enumerate(acvs):
            location_string = f"{acv.location:.2f}".rjust(self.column_width - 1) + " "

            if acv.observed_distance:
                distance_string = f"{acv.observed_distance:.2f}".rjust(self.column_width - 1) + " "
            else:
                distance_string = "NONE".center(self.column_width - 1) + " "

            if i in failed_sensors and i in ignored_sensors:
                distance_string = Back.GREEN + distance_string + Back.RESET
            elif i in failed_sensors:
                distance_string = Back.YELLOW + distance_string + Back.RESET
            elif i in ignored_sensors:
                distance_string = Back.BLUE + distance_string + Back.RESET

            speed_string = f"{acv.speed:.2f}".rjust(self.column_width - 1) + " "

            print("||" + "|".join([location_string, distance_string, speed_string]), end="")
        print()


LOGGER = Logger()
