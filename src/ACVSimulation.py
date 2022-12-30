import subject

from mapek.Knowledge import Knowledge
from mapek.Monitor import Monitor
from mapek.Analyzer import Analyzer
from mapek.Planner import Planner
from mapek.Executer import Executer
from subject.DistanceSensor import DistanceSensor

def run_simulation():
    """Runs the ACV simulation."""
    knowledge = Knowledge()
    knowledge.ideal_distance = subject.IDEAL_DISTANCE

    sensor = DistanceSensor()

    executer = Executer(sensor)
    planner = Planner(executer)
    analyzer = Analyzer(planner)
    monitor = Monitor(analyzer)

    sensor.register(monitor)
    sensor.read_data()

if __name__ == '__main__':
    run_simulation()