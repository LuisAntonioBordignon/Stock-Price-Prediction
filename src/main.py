from lib.environment import Environment
from src.models import *


model = MLP()
env = Environment(model)

env.fit()
