from pathlib import Path

from loader import prepare_data
from regressors import CatBoost, LGB, XGB


def train():
    sources = Path("data").rglob("*.jsonl")
    for source in sources:
        X, y = prepare_data(source)
        print(f"Training model on {source} with {len(X)} records")
        break

    cat = CatBoost()
    print(cat.feature_preprocessors())
    print(cat.prepare_pipeline())
    print(cat.prepare_grid_search())


if __name__ == "__main__":
    train()
