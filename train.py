from algrithm.ddqn.ddqn import DDQN
from environment import Environment

env = Environment()
ddqn = DDQN(env)
ddqn.train()

