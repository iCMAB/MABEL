import subject

from mapek.Knowledge import Knowledge
from mapek.Monitor import Monitor
from mapek.Analyzer import Analyzer
from mapek.Planner import Planner
from mapek.Executer import Executer
from subject.ACVUpdater import ACVUpdater

from ml_models.linearUCB import LinearUCB
from ml_models.linearTS import LinearThompsonSampling

def run_simulation():
    """Runs the ACV simulation."""
    
    knowledge = Knowledge()
    knowledge.ideal_distance = subject.IDEAL_DISTANCE

    d = 1
    alpha = 0.1
    # knowledge.model = LinearUCB(d, alpha)

    knowledge.model = LinearThompsonSampling(d)

    updater = ACVUpdater()

    executer = Executer(updater)
    planner = Planner(executer)
    analyzer = Analyzer(planner)
    monitor = Monitor(analyzer)


    updater.register(monitor)
    updater.read_data()

if __name__ == '__main__':
    run_simulation()