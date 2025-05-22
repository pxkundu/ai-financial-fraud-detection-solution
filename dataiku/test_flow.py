import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from io import StringIO
import contextlib

# Add the plugins directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
plugins_dir = os.path.join(current_dir, 'plugins', 'custom_recipes')
sys.path.append(plugins_dir)

# Create plots directory
plots_dir = os.path.join(current_dir, 'plots')
os.makedirs(plots_dir, exist_ok=True)

# Create tests directory and output file
tests_dir = os.path.join(current_dir, 'tests')
os.makedirs(tests_dir, exist_ok=True)
output_file = os.path.join(tests_dir, 'testOutput.md')

from feature_engineering import process_transaction_features, compute_aggregate_features

def generate_test_data(n_samples=1000):
    """Generate synthetic transaction data for testing."""
    np.random.seed(42)
    
    # Generate timestamps
    base_time = datetime.now() - timedelta(days=30)
    timestamps = [base_time + timedelta(hours=i) for i in range(n_samples)]
    
    # Generate transaction data
    data = {
        'transaction_id': [f'TX{i:06d}' for i in range(n_samples)],
        'timestamp': timestamps,
        'customer_id': [f'CUST{np.random.randint(1, 100):03d}' for _ in range(n_samples)],
        'merchant_id': [f'MERCH{np.random.randint(1, 50):03d}' for _ in range(n_samples)],
        'amount': np.random.lognormal(mean=4, sigma=1, size=n_samples),
        'location': [f'LOC{np.random.randint(1, 20):03d}' for _ in range(n_samples)],
        'device_id': [f'DEV{np.random.randint(1, 10):03d}' for _ in range(n_samples)],
        'is_fraud': np.random.binomial(1, 0.1, size=n_samples)  # 10% fraud rate
    }
    
    return pd.DataFrame(data)

def validate_features(df_processed):
    """Validate the engineered features."""
    print("\n=== Feature Validation ===")
    
    # Check for missing values
    missing_values = df_processed.isnull().sum()
    if missing_values.any():
        print("WARNING: Missing values found:")
        print(missing_values[missing_values > 0])
    else:
        print("✓ No missing values found")
    
    # Check for infinite values
    inf_values = np.isinf(df_processed.select_dtypes(include=[np.number])).sum()
    if inf_values.any():
        print("WARNING: Infinite values found:")
        print(inf_values[inf_values > 0])
    else:
        print("✓ No infinite values found")
    
    # Check for negative amounts
    if (df_processed['amount'] < 0).any():
        print("WARNING: Negative amounts found")
    else:
        print("✓ No negative amounts found")
    
    # Check feature correlations
    numeric_cols = df_processed.select_dtypes(include=[np.number]).columns
    correlations = df_processed[numeric_cols].corr()['is_fraud'].sort_values(ascending=False)
    print("\nTop 5 features correlated with fraud:")
    print(correlations[1:6])  # Exclude is_fraud itself

def plot_feature_distributions(df_processed):
    """Plot distributions of key features."""
    print("\n=== Feature Distributions ===")
    
    # Plot amount distributions by fraud status
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df_processed, x='amount', hue='is_fraud', bins=50)
    plt.title('Transaction Amount Distribution by Fraud Status')
    plt.savefig(os.path.join(plots_dir, 'amount_distribution.png'))
    plt.close()
    
    # Plot time-based features
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    sns.boxplot(data=df_processed, x='is_fraud', y='hour')
    plt.title('Transaction Hour by Fraud Status')
    
    plt.subplot(1, 2, 2)
    sns.boxplot(data=df_processed, x='is_fraud', y='day_of_week')
    plt.title('Day of Week by Fraud Status')
    plt.savefig(os.path.join(plots_dir, 'time_features.png'))
    plt.close()
    
    # Plot behavioral features
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    sns.boxplot(data=df_processed, x='is_fraud', y='merchant_risk_score')
    plt.title('Merchant Risk Score by Fraud Status')
    
    plt.subplot(1, 2, 2)
    sns.boxplot(data=df_processed, x='is_fraud', y='customer_risk_score')
    plt.title('Customer Risk Score by Fraud Status')
    plt.savefig(os.path.join(plots_dir, 'risk_scores.png'))
    plt.close()

def test_feature_engineering():
    """Test the feature engineering pipeline."""
    print("\n=== Testing Feature Engineering ===")
    
    # Generate test data
    df = generate_test_data(1000)
    print(f"Generated {len(df)} test transactions")
    print(f"Number of unique customers: {df['customer_id'].nunique()}")
    print(f"Number of unique merchants: {df['merchant_id'].nunique()}")
    print(f"Fraud rate: {df['is_fraud'].mean():.2%}")
    
    # Process features
    df_processed = process_transaction_features(df)
    print(f"\nProcessed features shape: {df_processed.shape}")
    
    # Validate features
    validate_features(df_processed)
    
    # Plot feature distributions
    plot_feature_distributions(df_processed)
    
    # Show detailed statistics
    print("\n=== Detailed Statistics ===")
    print("\nAmount Statistics:")
    print(df_processed[['amount', 'amount_log', 'amount_zscore']].describe())
    
    print("\nTime-based Statistics:")
    print(df_processed[['hour', 'day_of_week', 'is_weekend']].describe())
    
    print("\nBehavioral Statistics:")
    print(df_processed[['merchant_risk_score', 'customer_risk_score', 'location_change', 'device_change']].describe())
    
    # Compute aggregate features
    df_aggregate = compute_aggregate_features(df_processed)
    print(f"\nAggregate features shape: {df_aggregate.shape}")
    
    # Show customer-level statistics
    print("\nCustomer-level Statistics:")
    print(df_aggregate.describe())
    
    # Plot customer-level distributions
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    sns.histplot(data=df_aggregate, x='amount_mean', bins=30)
    plt.title('Average Transaction Amount per Customer')
    
    plt.subplot(1, 2, 2)
    sns.histplot(data=df_aggregate, x='is_fraud_mean', bins=30)
    plt.title('Average Fraud Rate per Customer')
    plt.savefig(os.path.join(plots_dir, 'customer_statistics.png'))
    plt.close()
    
    return df_processed, df_aggregate

def main():
    """Run the test and save output to markdown file."""
    print("Starting feature engineering test...")
    
    # Capture all output
    output = StringIO()
    with contextlib.redirect_stdout(output):
        df_processed, df_aggregate = test_feature_engineering()
        print("\nTest completed successfully!")
        print(f"\nPlots have been saved to: {plots_dir}")
    
    # Get the captured output
    output_text = output.getvalue()
    
    # Create markdown content
    md_content = f"""# Feature Engineering Test Output

## Test Results
```
{output_text}
```

## Generated Plots
The following plots were generated during the test:
1. `amount_distribution.png` - Transaction amount distribution by fraud status
2. `time_features.png` - Time-based feature distributions
3. `risk_scores.png` - Risk score distributions
4. `customer_statistics.png` - Customer-level statistics

## Test Summary
- Number of transactions processed: {len(df_processed)}
- Number of unique customers: {df_processed['customer_id'].nunique()}
- Number of features generated: {len(df_processed.columns)}
- Number of aggregate features: {len(df_aggregate.columns)}
- Fraud rate in test data: {df_processed['is_fraud'].mean():.2%}

## Feature Statistics
### Amount Features
{df_processed[['amount', 'amount_log', 'amount_zscore']].describe().to_markdown()}

### Time Features
{df_processed[['hour', 'day_of_week', 'is_weekend']].describe().to_markdown()}

### Behavioral Features
{df_processed[['merchant_risk_score', 'customer_risk_score', 'location_change', 'device_change']].describe().to_markdown()}

### Customer-Level Aggregates
{df_aggregate.describe().to_markdown()}
"""
    
    # Save to markdown file
    with open(output_file, 'w') as f:
        f.write(md_content)
    
    print(f"\nTest output has been saved to: {output_file}")

if __name__ == "__main__":
    main() 