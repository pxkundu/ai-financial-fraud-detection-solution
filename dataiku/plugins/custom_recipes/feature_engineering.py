import dataiku
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

def process_transaction_features(df):
    """Process transaction data and create features for fraud detection."""
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Time-based features
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    # Transaction amount features
    df['amount_log'] = np.log1p(df['amount'])
    df['amount_zscore'] = df.groupby('customer_id')['amount'].transform(
        lambda x: (x - x.mean()) / x.std()
    )
    
    # Frequency features
    df['transaction_count_24h'] = df.groupby('customer_id')['timestamp'].transform(
        lambda x: x.rolling('24H', min_periods=1).count()
    )
    
    # Velocity features
    df['amount_velocity_24h'] = df.groupby('customer_id')['amount'].transform(
        lambda x: x.rolling('24H', min_periods=1).sum()
    )
    
    # Location-based features
    df['location_change'] = df.groupby('customer_id')['location'].transform(
        lambda x: x != x.shift()
    ).astype(int)
    
    # Device-based features
    df['new_device'] = df.groupby('customer_id')['device_id'].transform(
        lambda x: x != x.shift()
    ).astype(int)
    
    # Merchant-based features
    merchant_risk = df.groupby('merchant_id')['is_fraud'].mean()
    df['merchant_risk_score'] = df['merchant_id'].map(merchant_risk)
    
    # Customer-based features
    customer_risk = df.groupby('customer_id')['is_fraud'].mean()
    df['customer_risk_score'] = df['customer_id'].map(customer_risk)
    
    # Time since last transaction
    df['time_since_last_tx'] = df.groupby('customer_id')['timestamp'].transform(
        lambda x: x.diff().dt.total_seconds()
    )
    
    # Amount ratio to average
    df['amount_ratio_to_avg'] = df.groupby('customer_id').apply(
        lambda x: x['amount'] / x['amount'].mean()
    ).reset_index(level=0, drop=True)
    
    return df

def compute_aggregate_features(df, window='24H'):
    """Compute aggregate features over a time window."""
    
    agg_features = df.groupby('customer_id').agg({
        'amount': ['mean', 'std', 'min', 'max', 'sum'],
        'transaction_count_24h': 'max',
        'location_change': 'sum',
        'new_device': 'sum'
    }).reset_index()
    
    agg_features.columns = ['customer_id'] + [f'{col[0]}_{col[1]}' for col in agg_features.columns[1:]]
    
    return agg_features

def main():
    # Get input dataset
    input_dataset = dataiku.Dataset("transactions")
    df = input_dataset.get_dataframe()
    
    # Process features
    df_processed = process_transaction_features(df)
    
    # Compute aggregate features
    agg_features = compute_aggregate_features(df_processed)
    
    # Merge features
    final_df = pd.merge(df_processed, agg_features, on='customer_id', how='left')
    
    # Scale numerical features
    scaler = StandardScaler()
    numerical_cols = [
        'amount', 'amount_log', 'amount_zscore', 'transaction_count_24h',
        'amount_velocity_24h', 'merchant_risk_score', 'customer_risk_score',
        'time_since_last_tx', 'amount_ratio_to_avg'
    ]
    
    final_df[numerical_cols] = scaler.fit_transform(final_df[numerical_cols])
    
    # Save processed dataset
    output_dataset = dataiku.Dataset("processed_transactions")
    output_dataset.write_with_schema(final_df)

if __name__ == "__main__":
    main() 