import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler

def process_transaction_features(df):
    """Process transaction data and create relevant features."""
    # Convert timestamp to datetime if it's not already
    if not isinstance(df['timestamp'].iloc[0], datetime):
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Sort by timestamp to ensure proper rolling window calculations
    df = df.sort_values(['customer_id', 'timestamp'])
    
    # Time-based features
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    # Transaction amount features
    df['amount_log'] = np.log1p(df['amount'])
    df['amount_zscore'] = (df['amount'] - df['amount'].mean()) / df['amount'].std()
    
    # Frequency features - using a fixed window size instead of time-based
    df['transaction_count_24h'] = df.groupby('customer_id').rolling(
        window=24, min_periods=1
    )['timestamp'].count().reset_index(level=0, drop=True)
    
    # Velocity features - using a fixed window size
    df['amount_sum_24h'] = df.groupby('customer_id').rolling(
        window=24, min_periods=1
    )['amount'].sum().reset_index(level=0, drop=True)
    
    # Location and device features
    df['location_change'] = df.groupby('customer_id')['location'].transform(
        lambda x: x != x.shift()
    ).astype(int)
    
    df['device_change'] = df.groupby('customer_id')['device_id'].transform(
        lambda x: x != x.shift()
    ).astype(int)
    
    # Risk scores
    df['merchant_risk_score'] = df.groupby('merchant_id')['is_fraud'].transform('mean')
    df['customer_risk_score'] = df.groupby('customer_id')['is_fraud'].transform('mean')
    
    # Time since last transaction
    df['time_since_last_tx'] = df.groupby('customer_id')['timestamp'].transform(
        lambda x: x.diff().dt.total_seconds()
    )
    
    # Amount ratio to average
    df['amount_ratio_to_avg'] = df['amount'] / df.groupby('customer_id')['amount'].transform('mean')
    
    return df

def compute_aggregate_features(df, window='24H'):
    """Compute aggregate features over a time window."""
    # Simple aggregation by customer_id
    agg_features = df.groupby('customer_id').agg({
        'amount': ['mean', 'std', 'min', 'max', 'sum'],
        'transaction_count_24h': 'mean',
        'location_change': 'sum',
        'device_change': 'sum',
        'is_fraud': 'mean'
    }).reset_index()
    
    # Flatten column names
    agg_features.columns = ['_'.join(col).strip() for col in agg_features.columns.values]
    
    return agg_features

if __name__ == "__main__":
    # Test the functions with sample data
    test_data = pd.DataFrame({
        'transaction_id': ['TX001', 'TX002', 'TX003'],
        'timestamp': pd.date_range(start='2024-01-01', periods=3, freq='H'),
        'customer_id': ['CUST001', 'CUST001', 'CUST002'],
        'merchant_id': ['MERCH001', 'MERCH002', 'MERCH001'],
        'amount': [100, 200, 150],
        'location': ['LOC001', 'LOC002', 'LOC001'],
        'device_id': ['DEV001', 'DEV001', 'DEV002'],
        'is_fraud': [0, 1, 0]
    })
    
    processed_data = process_transaction_features(test_data)
    print("Processed features shape:", processed_data.shape)
    print("\nProcessed features columns:", processed_data.columns.tolist())
    
    aggregate_data = compute_aggregate_features(processed_data)
    print("\nAggregate features shape:", aggregate_data.shape)
    print("\nAggregate features columns:", aggregate_data.columns.tolist()) 