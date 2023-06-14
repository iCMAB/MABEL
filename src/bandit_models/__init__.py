from .mab_model import MABModel

from .random import Random
from .linear_ucb import LinearUCB
# from .linear_TS import LinearThompsonSampling
from .epsilon_greedy import EpsilonGreedy
# from .UCB1 import UCB1_Normal_Penalized
# from .bootstrapped_UCB import BootstrappedUCB
# from .softmax_explorer import SoftmaxExplorer

MODELS = {
    "Random": Random,
    "LinearUCB": LinearUCB,
    # "LinearTS": LinearThompsonSampling,
    "EpsilonGreedy": EpsilonGreedy,
    # "UCB1": UCB1_Normal_Penalized,
    # "BootstrappedUCB": BootstrappedUCB,
    # "SoftmaxExplorer": SoftmaxExplorer,
}