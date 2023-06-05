from .bootstrapped_UCB import BootstrappedUCB
from .epsilon_greedy import EpsilonGreedy
from .linear_TS import LinearThompsonSampling
from .linear_UCB import LinearUCB
from .softmax_explorer import SoftmaxExplorer
from .UCB1 import UCB1_Normal_Penalized

MODELS = [
    ('LinearUCB', LinearUCB),
    ('LinearTS', LinearThompsonSampling),
    ('EpsilonGreedy', EpsilonGreedy),
    ('UCB1', UCB1_Normal_Penalized),
    ('BootstrappedUCB', BootstrappedUCB),
    ('SoftmaxExplorer', SoftmaxExplorer),
]
