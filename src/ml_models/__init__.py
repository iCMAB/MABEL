from .linearUCB import LinearUCB
from .linearTS import LinearThompsonSampling
from .EpsilonGreedy import EpsilonGreedy
from .UCB1 import UCB1_Normal_Penalized
from .bootstrappedUCB import BootstrappedUCB
from .SoftmaxExplorer import SoftmaxExplorer

MODELS = {
    'LinearUCB': LinearUCB,
    'LinearTS': LinearThompsonSampling,
    'EpsilonGreedy': EpsilonGreedy,
    'UCB1': UCB1_Normal_Penalized,
    'BootstrappedUCB': BootstrappedUCB,
    'SoftmaxExplorer': SoftmaxExplorer,
}
