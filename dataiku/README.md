# Dataiku Integration for AI-Powered Financial Fraud Detection

This directory contains the Dataiku integration components for the AI-powered financial fraud detection solution. It includes custom recipes, flows, and monitoring components that work together with AWS services to provide comprehensive fraud detection capabilities.

## Directory Structure

```
dataiku/
├── flows/
│   └── fraud_detection_flow.json    # Main fraud detection flow configuration
├── plugins/
│   └── custom_recipes/
│       ├── feature_engineering.py   # Feature engineering recipe
│       ├── model_training.py        # Model training recipe
│       └── model_monitoring.py      # Model monitoring recipe
└── requirements.txt                 # Python dependencies
```

## Components

### 1. Fraud Detection Flow (`flows/fraud_detection_flow.json`)
The main flow configuration that orchestrates the entire fraud detection pipeline:
- Data ingestion from S3 and Textract
- Feature engineering and data validation
- Model training with multiple algorithms
- AWS Bedrock integration
- EKS deployment configuration
- Real-time monitoring and drift detection

### 2. Custom Recipes

#### Feature Engineering (`plugins/custom_recipes/feature_engineering.py`)
Processes transaction data and creates relevant features:
- Time-based features (hour, day of week, weekend)
- Transaction amount features (log, z-score)
- Frequency and velocity features
- Location and device-based features
- Merchant and customer risk scores
- Aggregate features over time windows
- Feature scaling and normalization

#### Model Training (`plugins/custom_recipes/model_training.py`)
Implements multiple models and selects the best one:
- Multiple model implementations (XGBoost, LightGBM, Random Forest, Gradient Boosting)
- Automated model selection based on performance
- Cross-validation and hyperparameter tuning
- Model evaluation with precision-recall curves
- Model metadata tracking
- S3 integration for model storage
- Feature importance analysis

#### Model Monitoring (`plugins/custom_recipes/model_monitoring.py`)
Tracks model performance and data drift:
- Real-time performance monitoring
- Data drift detection using Kolmogorov-Smirnov test
- Prometheus metrics integration
- Grafana dashboard support
- Automated alerting
- S3 integration for monitoring results
- Comprehensive logging

## Prerequisites

- Dataiku DSS 11.0 or later
- Python 3.9 or later
- AWS credentials with appropriate permissions
- Required Python packages (see requirements.txt)

## Installation

1. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure AWS credentials:
   ```bash
   aws configure
   ```

3. Set up environment variables:
   ```bash
   export AWS_REGION=us-east-1
   export S3_BUCKET_NAME=fraud-detection-data
   export BEDROCK_ENDPOINT=https://bedrock.us-east-1.amazonaws.com
   export EKS_CLUSTER_NAME=fraud-detection-cluster
   ```

## Usage

1. Deploy the fraud detection flow:
   ```python
   import dataiku
   import json
   
   with open('flows/fraud_detection_flow.json', 'r') as f:
       flow = json.load(f)
   dataiku.deploy_flow(flow)
   ```

2. Run feature engineering:
   ```python
   from dataiku.customrecipe import get_recipe_config
   from feature_engineering import process_transaction_features
   
   # Get input dataset
   input_dataset = dataiku.Dataset("transactions")
   df = input_dataset.get_dataframe()
   
   # Process features
   df_processed = process_transaction_features(df)
   ```

3. Train models:
   ```python
   from model_training import FraudDetectionModel
   
   model = FraudDetectionModel(model_type='xgboost')
   model.train(X_train, y_train)
   model.save_model('models/fraud_detection_xgboost.joblib')
   ```

4. Monitor model performance:
   ```python
   from model_monitoring import ModelMonitor
   
   monitor = ModelMonitor(
       model_path="fraud_detection_xgboost.joblib",
       metadata_path="fraud_detection_xgboost.joblib_metadata.json"
   )
   monitor.monitor_predictions(X_test)
   ```

## Monitoring

The solution includes comprehensive monitoring capabilities:
- Real-time model performance metrics
- Data drift detection
- System health monitoring
- Automated alerts for anomalies

Access monitoring dashboards:
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090

## Best Practices

1. **Data Validation**
   - Validate input data before processing
   - Use Great Expectations for data quality checks
   - Monitor data drift regularly

2. **Model Management**
   - Version control all models
   - Track model metadata
   - Monitor model performance
   - Implement automated retraining

3. **Security**
   - Use AWS IAM roles
   - Encrypt sensitive data
   - Implement proper access controls
   - Monitor for security threats

4. **Performance**
   - Optimize feature engineering
   - Use efficient data structures
   - Implement caching where appropriate
   - Monitor resource usage

## Troubleshooting

Common issues and solutions:

1. **Data Access Issues**
   - Verify AWS credentials
   - Check S3 bucket permissions
   - Validate IAM roles

2. **Model Performance Issues**
   - Check for data drift
   - Verify feature engineering
   - Monitor resource usage
   - Review model metrics

3. **Integration Issues**
   - Verify AWS service endpoints
   - Check network connectivity
   - Validate configuration settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

# Dataiku Feature Engineering Tests

This directory contains the feature engineering pipeline for the AI-powered financial fraud detection solution. The tests validate the feature engineering process and data transformations.

## Directory Structure

```
dataiku/
├── plugins/
│   └── custom_recipes/
│       ├── feature_engineering.py
│       ├── model_training.py
│       └── model_monitoring.py
├── flows/
│   └── fraud_detection_flow.json
└── test_flow.py
```

## Running the Tests

1. Ensure you have the required dependencies:
```bash
pip install pandas numpy scikit-learn
```

2. Run the test script:
```bash
python3 test_flow.py
```

## Test Output Explanation

The test generates and processes synthetic transaction data to validate the feature engineering pipeline:

1. **Data Generation**:
   - Creates 1000 synthetic transactions
   - Includes customer IDs, merchant IDs, amounts, locations, and fraud flags
   - 10% of transactions are marked as fraudulent

2. **Feature Engineering**:
   - Processes raw transactions into 21 engineered features
   - Features include time-based, amount-based, and behavioral indicators
   - All features are calculated at the transaction level

3. **Aggregation**:
   - Aggregates features by customer_id
   - Creates 10 customer-level features
   - Reduces data from 1000 transactions to 99 customer profiles

## Feature Descriptions

### Transaction-Level Features (21 total)
- **Time Features**:
  - hour: Hour of transaction
  - day_of_week: Day of week (0-6)
  - is_weekend: Binary indicator for weekend transactions

- **Amount Features**:
  - amount_log: Log-transformed transaction amount
  - amount_zscore: Z-score normalized amount

- **Frequency Features**:
  - transaction_count_24h: Number of transactions in last 24 hours
  - amount_sum_24h: Total amount in last 24 hours

- **Behavioral Features**:
  - location_change: Indicator for location change
  - device_change: Indicator for device change
  - merchant_risk_score: Historical fraud rate by merchant
  - customer_risk_score: Historical fraud rate by customer
  - time_since_last_tx: Time since last transaction
  - amount_ratio_to_avg: Ratio to customer's average amount

### Customer-Level Features (10 total)
- **Amount Statistics**:
  - amount_mean: Average transaction amount
  - amount_std: Standard deviation of amounts
  - amount_min: Minimum transaction amount
  - amount_max: Maximum transaction amount
  - amount_sum: Total transaction amount

- **Behavioral Statistics**:
  - transaction_count_24h_mean: Average daily transaction count
  - location_change_sum: Total location changes
  - device_change_sum: Total device changes
  - is_fraud_mean: Average fraud rate

## Expected Output

The test should show:
1. Number of transactions generated
2. Shape of processed features (1000, 21)
3. Shape of aggregated features (99, 10)
4. Sample values for key features

## Troubleshooting

If you encounter issues:
1. Check Python version (3.8+ required)
2. Verify all dependencies are installed
3. Ensure you're in the correct directory
4. Check file permissions

## Next Steps

After running the tests:
1. Review the feature distributions
2. Validate the aggregation logic
3. Check for any data quality issues
4. Proceed to model training if all tests pass 