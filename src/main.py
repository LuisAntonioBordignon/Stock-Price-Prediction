from lib.environment import Environment
from src.models import *
from pathlib import Path

tickers = list(Path("data/tickers/").glob("**/"))[1:]

for ticker in tickers:

    model = MLP()
    env = Environment(model)

    histories = env.fit(ticker=ticker.name, training_days=5)

    print(f"histories: {histories}")
