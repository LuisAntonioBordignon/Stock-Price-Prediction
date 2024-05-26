import os

from lib.environment import Environment
from models import *


model = MLP()
env = Environment(model)

env.fit()
