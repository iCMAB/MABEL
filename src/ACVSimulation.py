import subject

from mapek.Knowledge import Knowledge
from mapek.Monitor import Monitor
from mapek.Analyzer import Analyzer
from mapek.Planner import Planner
from mapek.Executer import Executer
from subject.ACVUpdater import ACVUpdater

def run_simulation():
    """Runs the ACV simulation."""
    knowledge = Knowledge()
    knowledge.ideal_distance = subject.IDEAL_DISTANCE

    updater = ACVUpdater()

    executer = Executer(updater)
    planner = Planner(executer)
    analyzer = Analyzer(planner)
    monitor = Monitor(analyzer)

    updater.register(monitor)
    updater.read_data()

if __name__ == '__main__':
    run_simulation()