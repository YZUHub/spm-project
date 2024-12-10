from abc import ABC, abstractmethod
from pathlib import Path

import jsonlines
import pandas as pd
from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor


class Regressor(ABC):
    def __init__(self):
        self.regressor = None
        self.categorical_features = ['unit_type', 'building_type_name_aggregated', 'energy_label', 'ownership_form']
        self.features = [
            "postal_code",
            "unit_type",
            "building_type_name_aggregated",
            "floor_number",
            "floors",
            "land_area",
            "bta",
            "bra",
            "prom",
            "rooms",
            "bedrooms",
            "bathrooms",
            "built_year",
            "energy_label",
            "bar",
            "wcs",
            "building_enr",
            "ownership_form",
            "nearest_train_station_distance",
            "nearest_bus_station_distance",
            "nearest_ferry_terminal_distance",
            "nearest_tram_station_distance",
            "nearest_underground_station_distance",
            "nearest_gondola_lift_station_distance",
            "nearest_airport_distance",
            "nearest_kindergartens_distance",
            "nearest_elementary_middle_school_distance",
            "nearest_high_school_distance",
            "nearest_fire_station_distance",
            "in_beach_zone",
            "date",
            "lat",
            "lon",
            "year",
            "month",
        ]

    @abstractmethod
    def get_grid_params(self) -> dict:
        return {}

    def load_data(self, filename: str) -> tuple[pd.DataFrame, pd.Series]:
        with jsonlines.open(filename) as reader:
            df = pd.DataFrame(reader)

        df["lat"] = df["geometry"].apply(lambda x: x["coordinates"][1])
        df["lon"] = df["geometry"].apply(lambda x: x["coordinates"][0])
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month

        return df[self.features], df["index"]

    def feature_preprocessors(self) -> ColumnTransformer:
        # Create preprocessor (only for categorical features)
        encoder = OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")
        preprocessor = ColumnTransformer(transformers=[("cat", encoder, self.categorical_features)], remainder="passthrough")
        return preprocessor

    def prepare_pipeline(self) -> Pipeline:
        return Pipeline([
            ("preprocessor", self.feature_preprocessors()),
            ("regressor", self.regressor),
        ])

    def prepare_grid_search(self):
        pipeline = self.prepare_pipeline()
        params = self.get_grid_params()
        grid_search = GridSearchCV(pipeline, params, cv=3, n_jobs=-1, verbose=2)
        return grid_search


class CatBoost(Regressor):
    def __init__(self):
        super().__init__()
        self.regressor = CatBoostRegressor(verbose=False, random_state=42)

    def get_grid_params(self) -> dict:
        return {
            'regressor__n_estimators': [100, 200, 300],
            'regressor__learning_rate': [0.01, 0.1, 0.3],
            'regressor__max_depth': [3, 4, 5],
            'regressor__l2_leaf_reg': [1, 3, 5],
            'regressor__subsample': [0.8, 0.9, 1.0],
            'regressor__colsample_bylevel': [0.8, 0.9, 1.0]
        }


class LGB(Regressor):
    def __init__(self):
        super().__init__()
        self.regressor = LGBMRegressor(random_state=42)

    def get_grid_params(self) -> dict:
        return {
            'regressor__n_estimators': [100, 200, 300],
            'regressor__learning_rate': [0.01, 0.1, 0.3],
            'regressor__max_depth': [3, 4, 5],
            'regressor__num_leaves': [7, 15, 31],
            'regressor__subsample': [0.8, 0.9, 1.0],
            'regressor__colsample_bytree': [0.8, 0.9, 1.0]
        }


class XGB(Regressor):
    def __init__(self):
        super().__init__()
        self.regressor = XGBRegressor(tree_method="hist", random_state=42)

    def get_grid_params(self) -> dict:
        return {
            'regressor__n_estimators': [100, 200, 300],
            'regressor__learning_rate': [0.01, 0.1, 0.3],
            'regressor__max_depth': [3, 4, 5],
            'regressor__min_child_weight': [1, 3, 5],
            'regressor__subsample': [0.8, 0.9, 1.0],
            'regressor__colsample_bytree': [0.8, 0.9, 1.0]
        }
