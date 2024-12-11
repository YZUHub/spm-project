from abc import ABC, abstractmethod
from typing import Iterator

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import BaseCrossValidator, GridSearchCV
from xgboost import XGBRegressor


class TimeseriesSplitter(BaseCrossValidator):
    def __init__(self, n_splits: int = 3):
        self.validation_folds = [[2014, 2016], [2017, 2019], [2020, 2022]]
        self.n_splits = n_splits

    def split(self, X: pd.DataFrame, y: pd.Series, groups: None = None) -> Iterator[tuple[np.ndarray, np.ndarray]]:
        for validation_years in self.validation_folds:
            train_indices = X[X["year"] < validation_years[0]].index
            val_indices = X[X["year"].isin(validation_years)].index
            yield train_indices, val_indices

    def get_n_splits(self, X=None, y=None, groups=None):
        """Returns the number of splitting iterations"""
        return self.n_splits


class Regressor(ABC):
    def __init__(self):
        self.regressor = None
        self.test_years = [2023, 2024]
        self.cv_splitter = TimeseriesSplitter()
        self.best_model = None
        self.cv_results = None

    @abstractmethod
    def get_grid_params(self) -> dict:
        return {}

    def load_data(self) -> tuple[pd.DataFrame, pd.Series]:
        df = pd.read_csv("data/timeseries-sample.csv")
        df = df.drop(columns=[df.columns[0]])
        print(f"Successfully loaded data with shape {df.shape = }")
        df["in_beach_zone"] = df["in_beach_zone"].astype(int)

        X, y = df.drop(columns=["index"]), df["index"]
        return X, y

    def train_test_split(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        X, y = self.load_data()
        X_train, X_test = X[X["year"].isin(self.test_years) == False], X[X["year"].isin(self.test_years)]
        y_train, y_test = y[X["year"].isin(self.test_years) == False], y[X["year"].isin(self.test_years)]
        print(f"Successfully split data into train and test sets with shapes {X_train.shape = }, {X_test.shape = }")
        return X_train, X_test, y_train, y_test

    def evaluate_model(self, y_true: pd.Series, y_pred: np.ndarray) -> dict:
        return {
            'MSE': mean_squared_error(y_true, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
            'MAE': mean_absolute_error(y_true, y_pred),
            'R2': r2_score(y_true, y_pred)
        }

    def grid_search(self, X: pd.DataFrame, y: np.ndarray) -> GridSearchCV:
        gs = GridSearchCV(
            self.regressor,
            self.get_grid_params(),
            scoring="neg_mean_squared_error",
            cv=self.cv_splitter,
            n_jobs=-1,
            verbose=3,
        )

        gs.fit(X, y)
        return gs


class CatBoost(Regressor):
    def __init__(self):
        super().__init__()
        self.regressor = CatBoostRegressor(verbose=False, random_state=42)

    def get_grid_params(self) -> dict:
        return {
            'iterations': [100, 200],
            'learning_rate': [0.01, 0.05],
            'depth': [4, 6],
            # 'l2_leaf_reg': [3, 5],
        }


class LightGBM(Regressor):
    def __init__(self):
        super().__init__()
        self.regressor = LGBMRegressor(random_state=42, verbose=-1)

    def get_grid_params(self) -> dict:
        return {
            'n_estimators': [100, 200],
            'learning_rate': [0.01, 0.05],
            'max_depth': [4, 6],
            # 'num_leaves': [31, 63],
        }


class XGBoost(Regressor):
    def __init__(self):
        super().__init__()
        self.regressor = XGBRegressor(tree_method="hist", random_state=42)

    def get_grid_params(self) -> dict:
        return {
            'n_estimators': [100, 200],
            'learning_rate': [0.01, 0.05],
            'max_depth': [4, 6],
            # 'min_child_weight': [1, 3, 5],
        }
