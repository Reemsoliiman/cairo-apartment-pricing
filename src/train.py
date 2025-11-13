import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor
import joblib
import pandas as pd
from src.utils.logger import get_logger

logger = get_logger(__name__)

MODELS = {
    'RandomForest': RandomForestRegressor(n_estimators=500, max_depth=20, random_state=42),
    'XGBoost': XGBRegressor(n_estimators=800, learning_rate=0.05, max_depth=8, random_state=42),
    'CatBoost': CatBoostRegressor(depth=10, learning_rate=0.03, verbose=0, random_state=42),
    'LightGBM': LGBMRegressor(n_estimators=1000, learning_rate=0.03, max_depth=10, random_state=42),
}

def train_all_models(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    best_mae = float('inf')
    best_model = None
    best_name = ""

    with mlflow.start_run(run_name=f"Training {pd.Timestamp.now().strftime('%Y-%m-%d')}"):
        for name, model in MODELS.items():
            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, pred)
            
            mlflow.log_metric(f"{name}_MAE", mae)
            mlflow.log_metric(f"{name}_RMSE", mean_squared_error(y_test, pred, squared=False))
            mlflow.log_metric(f"{name}_R2", r2_score(y_test, pred))
            mlflow.sklearn.log_model(model, f"models/{name}")
            
            if mae < best_mae:
                best_mae = mae
                best_model = model
                best_name = name
        
        mlflow.log_metric("best_MAE", best_mae)
        mlflow.set_tag("best_model", best_name)
        mlflow.set_tag("status", "production")
        
        joblib.dump(best_model, "models/best_model.pkl")
        logger.info(f"Best model: {best_name} | MAE: {best_mae:,.0f} EGP")