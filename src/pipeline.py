from src.preprocess import load_and_merge
from src.features import create_features
from src.train import train_all_models
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
import pandas as pd

if __name__ == "__main__":
    df = load_and_merge()
    df = create_features(df)
    
    feature_cols = [
        'area_sqm', 'bedrooms', 'bathrooms', 'floor_cat', 'building_age_years',
        'district', 'finishing_score', 'view_score', 'is_premium_compound',
        'proximity_score', 'has_amenities_full', 'price_per_sqm_usd'
    ]
    
    cat_cols = ['district']
    num_cols = [c for c in feature_cols if c not in cat_cols]
    
    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
    ])
    
    X = preprocessor.fit_transform(df[feature_cols])
    y = df['price_usd']
    
    train_all_models(X, y)