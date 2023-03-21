import subject

from mapek.Knowledge import Knowledge
from mapek.Monitor import Monitor
from mapek.Analyzer import Analyzer
from mapek.Planner import Planner
from mapek.Executer import Executer
from subject.ACVUpdater import ACVUpdater

from ml_models.linearUCB import LinearUCB
from ml_models.linearTS import LinearThompsonSampling
from ml_models.EpsilonGreedy import EpsilonGreedy
from ml_models.UCB1 import UCB1_Normal_Penalized
from ml_models.bootstrappedUCB import BootstrappedUCB

model_options = [
    ('LinearUCB', LinearUCB),
    ('LinearThompsonSampling', LinearThompsonSampling),
    ('BernoulliEpsilon', EpsilonGreedy),
    ('UCB1', UCB1_Normal_Penalized),
    ('BootstrappedUCB',BootstrappedUCB)
]


def run_simulation():
    """Runs the ACV simulation."""

    knowledge = Knowledge()
    updater = ACVUpdater()
    knowledge.ideal_distance = subject.IDEAL_DISTANCE
    
    model = select_model()

    d = 1
    alpha = 0.1
    epsilon = 0.5
    n_arms = len(updater.acvs) - 1
    n_bootstrap = 1000
    knowledge.mab_model = model(n_bootstrap = n_bootstrap,
        d=d, alpha=alpha, epsilon=epsilon, n_arms=n_arms)

   

    executer = Executer(updater)
    planner = Planner(executer)
    analyzer = Analyzer(planner)
    monitor = Monitor(analyzer)

    updater.register(monitor)
    updater.run_update_loop()


def select_model():
    """Selects the model to use for the simulation."""

    print("\nSelect a model:\n")
    for i, model in enumerate(model_options):
        print(f"{i + 1}. {model[0]}")

    print()

    selection = ""
    while (not selection.isdigit()) or (int(selection) not in range(1, len(model_options) + 1)):
        selection = input("Selection: ")

    return model_options[int(selection) - 1][1]


if __name__ == '__main__':
    run_simulation()
