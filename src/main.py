from os import environ

from acvs.acv_manager import ACVManager
from bandit_models import MABModel, MODELS
from utils import CONFIG

def main():
    model = initialize_model()
    run_simulation(model)

def run_simulation(model: MABModel):
    """Runs the ACV simulation."""
    manager = ACVManager(model)
    for _ in range(CONFIG["simulation"]["num_simulation_runs"]):
        manager.run_simulation()

def initialize_model() -> MABModel:
    """Selects the model to use for the simulation."""
    model_cls = MODELS[get_model()]

    return model_cls(
        n_arms=CONFIG["acvs"]["num_acvs"] + 1,
        # epsilon=float(CONFIG["mab"]["epsilon"]),
        # n_bootstrap=int(CONFIG["mab"]["n_bootstrap"]),
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
    print(CONFIG["logging"]["minor_divider"])

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
    main()
