from pathlib import Path

from sklearn.model_selection import GridSearchCV

from regressors import CatBoost, LightGBM, XGBoost


def train():
    cat = CatBoost()

    X_train, X_test, y_train, y_test = cat.train_test_split()

    cat_gs: GridSearchCV = cat.grid_search(X_train, y_train)
    print(f"{cat_gs.best_params_ = }")
    y_pred = cat_gs.predict(X_test)
    print(f"{cat.evaluate_model(y_test, y_pred) = }")

    lgbm = LightGBM()
    lgbm_gs = lgbm.grid_search(X_train, y_train)
    print(f"{lgbm_gs.best_params_ = }")
    y_pred = lgbm_gs.predict(X_test)
    print(f"{lgbm.evaluate_model(y_test, y_pred) = }")

    xgb = XGBoost()
    xgb_gs = xgb.grid_search(X_train, y_train)
    print(f"{xgb_gs.best_params_ = }")
    y_pred = xgb_gs.predict(X_test)
    print(f"{xgb.evaluate_model(y_test, y_pred) = }")


if __name__ == "__main__":
    train()
