from regressors import CatBoost, LightGBM, Regressor, XGBoost


def train():
    cat = CatBoost()

    X_train, X_test, y_train, y_test = cat.train_test_split()

    cat_gs = cat.grid_search(X_train, y_train)
    print(f"{cat_gs.best_params_ = }")
    y_pred = cat_gs.predict(X_test)
    print(f"CatBoost model metrics: {Regressor.evaluate_model(y_test, y_pred)}")

    lgbm = LightGBM()
    lgbm_gs = lgbm.grid_search(X_train, y_train)
    print(f"{lgbm_gs.best_params_ = }")
    y_pred = lgbm_gs.predict(X_test)
    print(f"LightGBM model metrics: {Regressor.evaluate_model(y_test, y_pred)}")

    xgb = XGBoost()
    xgb_gs = xgb.grid_search(X_train, y_train)
    print(f"{xgb_gs.best_params_ = }")
    y_pred = xgb_gs.predict(X_test)
    print(f"XGBoost model metrics: {Regressor.evaluate_model(y_test, y_pred)}")


if __name__ == "__main__":
    train()
