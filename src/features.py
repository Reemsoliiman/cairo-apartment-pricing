import pandas as pd

PREMIUM_COMPOUNDS = {
    'Katameya Heights', 'Hyde Park', 'Lake View', 'Palm Hills', 'Mountain View',
    'Katameya Dunes', 'Mivida', 'Eastown', 'The Address East'
}

def create_features(df):
    df = df.copy()
    
    df['is_premium_compound'] = df['compound_name'].apply(lambda x: 1 if x in PREMIUM_COMPOUNDS else 0)
    df['compound_name'] = df['compound_name'].fillna('None')
    
    df['finishing_score'] = df['finishing_type'].map({
        'Unfinished': 1, 'Semi-finished': 2, 'Lux': 3, 'Super Lux': 4
    }).fillna(2)
    
    df['view_score'] = df['view_type'].map({
        'Street': 1, 'Garden': 2, 'Compound': 3, 'Nile': 4
    }).fillna(1)
    
    df['floor_cat'] = pd.cut(df['floor_number'], bins=[0, 5, 10, 20], labels=[1, 2, 3]).astype(int)
    df['proximity_score'] = (10 / (df['distance_to_mall_km'] + 1)) + (5 / (df['distance_to_metro_km'] + 1))
    
    df['has_amenities_full'] = (
        (df['has_parking'] == 'Yes') &
        (df['has_security'] == 'Yes') &
        (df['has_amenities'] == 'Yes')
    ).astype(int)
    
    return df