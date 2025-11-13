import pandas as pd
from src.utils.logger import get_logger

logger = get_logger(__name__)

def load_and_merge():
    original = pd.read_csv('data/raw/cairo_real_estate_dataset.csv')
    scraped = pd.read_parquet('data/processed/scraped_latest.parquet')
    rates = pd.read_csv('data/processed/cbe_rates.csv')
    
    df = pd.concat([original, scraped], ignore_index=True)
    df = df[df['bedrooms'].isin([2, 3])]
    df = df[df['area_sqm'].between(70, 300)]
    df = df[df['price_egp'] < 15_000_000]
    
    df['listing_month'] = pd.to_datetime(df['listing_date']).dt.strftime('%Y-%m')
    df = df.merge(rates, on='listing_month', how='left')
    df['usd_rate'] = df['usd_rate'].fillna(40.0)
    
    df['price_usd'] = df['price_egp'] / df['usd_rate']
    df['price_per_sqm_usd'] = df['price_usd'] / df['area_sqm']
    
    logger.info(f"Preprocessed {len(df)} rows")
    return df