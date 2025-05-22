import pandas as pd
import numpy as np
from scipy import stats
import joblib
import json
from datetime import datetime
from sklearn.metrics import precision_score, recall_score, f1_score
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelMonitor:
    def __init__(self, model_path, metadata_path):
        """Initialize model monitor with trained model and metadata."""
        self.model = joblib.load(model_path)
        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)
        
        self.feature_importance = self.metadata.get('feature_importance', {})
        self.training_date = self.metadata.get('training_date')
        self.model_parameters = self.metadata.get('model_parameters', {})
        
        # Initialize drift detection thresholds
        self.drift_threshold = 0.1
        self.performance_threshold = 0.8
    
    def detect_drift(self, X):
        """Detect data drift using Kolmogorov-Smirnov test."""
        drift_metrics = {}
        
        for feature in X.columns:
            if feature in self.feature_importance:
                # Get feature distribution from training data
                train_dist = self.metadata.get('feature_distributions', {}).get(feature, {})
                
                if train_dist:
                    # Perform KS test
                    ks_stat, p_value = stats.ks_2samp(
                        train_dist['values'],
                        X[feature].values
                    )
                    
                    drift_metrics[feature] = {
                        'ks_statistic': float(ks_stat),
                        'p_value': float(p_value),
                        'drift_detected': p_value < self.drift_threshold
                    }
        
        return drift_metrics
    
    def monitor_predictions(self, X, y_true=None):
        """Monitor model predictions and detect drift."""
        # Get predictions
        y_pred = self.model.predict(X)
        y_pred_proba = self.model.predict_proba(X)[:, 1]
        
        # Initialize monitoring results
        monitoring_results = {
            'timestamp': datetime.now().isoformat(),
            'drift_metrics': self.detect_drift(X),
            'prediction_metrics': {}
        }
        
        # Calculate performance metrics if true labels are provided
        if y_true is not None:
            monitoring_results['prediction_metrics'] = {
                'precision': float(precision_score(y_true, y_pred)),
                'recall': float(recall_score(y_true, y_pred)),
                'f1_score': float(f1_score(y_true, y_pred))
            }
            
            # Check if performance has degraded
            for metric, value in monitoring_results['prediction_metrics'].items():
                if value < self.performance_threshold:
                    logger.warning(f"Performance degradation detected in {metric}: {value:.4f}")
        
        # Log drift detection results
        for feature, metrics in monitoring_results['drift_metrics'].items():
            if metrics['drift_detected']:
                logger.warning(
                    f"Data drift detected in feature {feature}: "
                    f"KS statistic = {metrics['ks_statistic']:.4f}, "
                    f"p-value = {metrics['p_value']:.4f}"
                )
        
        return monitoring_results

if __name__ == "__main__":
    # Test the monitor with sample data
    np.random.seed(42)
    n_samples = 1000
    
    # Generate sample features
    X = pd.DataFrame({
        'amount': np.random.lognormal(4, 1, n_samples),
        'transaction_count_24h': np.random.poisson(5, n_samples),
        'location_change': np.random.binomial(1, 0.1, n_samples),
        'device_change': np.random.binomial(1, 0.05, n_samples),
        'merchant_risk_score': np.random.beta(2, 5, n_samples),
        'customer_risk_score': np.random.beta(2, 5, n_samples)
    })
    
    # Generate target variable
    y = np.random.binomial(1, 0.1, n_samples)  # 10% fraud rate
    
    # Create sample model and metadata
    from model_training import FraudDetectionModel
    model = FraudDetectionModel(model_type='xgboost')
    X_test, y_test = model.train(X, y)
    model.save_model('test_model.joblib')
    
    # Initialize monitor
    monitor = ModelMonitor('test_model.joblib', 'test_model.joblib_metadata.json')
    
    # Monitor predictions
    monitoring_results = monitor.monitor_predictions(X_test, y_test)
    
    print("Monitoring results:")
    print(json.dumps(monitoring_results, indent=2)) 