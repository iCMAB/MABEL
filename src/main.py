from os import environ

from mapek import Knowledge, Monitor, Analyzer, Planner, Executer
from subject import ACVUpdater
from ml_models import MABModel, MODELS

from config import get_config


def run_simulation():
    """Runs the ACV simulation."""
    ideal_distance = get_config('acvs', 'ideal_distance')

    knowledge = Knowledge()

    knowledge.ideal_distance = ideal_distance
    knowledge.mab_model = initialize_model()

    num_sim_runs = get_config('simulation', 'num_simulation_runs')
    for _ in range(num_sim_runs):
        updater = ACVUpdater()
        executer = Executer(updater)
        planner = Planner(executer)
        analyzer = Analyzer(planner)
        monitor = Monitor(analyzer)

        updater.register(monitor)
        updater.run_update_loop()


def initialize_model() -> MABModel:
    """Selects the model to use for the simulation."""
    model_cls = MODELS[get_model()]

    d = get_config('mab', 'd')
    alpha = get_config('mab', 'alpha')
    epsilon = get_config('mab', 'epsilon')
    n_arms = get_config('acvs', 'num_acvs') - 1
    n_bootstrap = get_config('mab', 'n_bootstrap')
    ideal_distance = get_config('acvs', 'ideal_distance')

    return model_cls(
        d=d,
        n_arms=n_arms,
        ideal_distance=ideal_distance,
        alpha=alpha,
        epsilon=epsilon,
        n_bootstrap=n_bootstrap,
    )


def get_model() -> str:
    model_name = environ.get("MODEL")

    if model_name:
        if model_name in MODELS:
            return model_name
        else:
            print("Model not found, dropping to user input")

    # If the environment variable doesn't exist, get it from user input
    print("\nSelect a model:")
    print(get_config('output', 'minor_divider'))

    selector = {}
    for i, key in enumerate(MODELS.keys(), start=1):
        print(f"{i}. {key}")
        selector[i] = key

    print()

    selection = -1
    while selection not in selector:
        try:
            selection = int(input("Selection: "))
        except ValueError:
            # If it's not an int, we don't care that it fails because it won't match anyway
            pass

    return selector[selection]


if __name__ == '__main__':
    run_simulation()
