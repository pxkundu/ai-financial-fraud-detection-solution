import dataiku
import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score
import joblib
import boto3
import json
from datetime import datetime, timedelta
from prometheus_client import start_http_server, Gauge, Counter
import alibi_detect
from alibi_detect import drift
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelMonitor:
    def __init__(self, model_path, metadata_path, s3_bucket=None):
        self.model_path = model_path
        self.metadata_path = metadata_path
        self.s3_bucket = s3_bucket
        self.model = None
        self.metadata = None
        self.threshold = None
        self.feature_importance = None
        
        # Initialize Prometheus metrics
        self.precision_gauge = Gauge('model_precision', 'Model precision score')
        self.recall_gauge = Gauge('model_recall', 'Model recall score')
        self.f1_gauge = Gauge('model_f1', 'Model F1 score')
        self.drift_score_gauge = Gauge('data_drift_score', 'Data drift score')
        self.prediction_counter = Counter('model_predictions_total', 'Total number of predictions')
        self.fraud_counter = Counter('fraud_predictions_total', 'Total number of fraud predictions')
        
        # Load model and metadata
        self.load_model()
    
    def load_model(self):
        """Load model and metadata from local path or S3."""
        try:
            if self.s3_bucket:
                s3 = boto3.client('s3')
                s3.download_file(self.s3_bucket, f"models/{self.model_path}", self.model_path)
                s3.download_file(self.s3_bucket, f"models/{self.metadata_path}", self.metadata_path)
            
            self.model = joblib.load(self.model_path)
            with open(self.metadata_path, 'r') as f:
                self.metadata = json.load(f)
            
            self.threshold = self.metadata['threshold']
            self.feature_importance = pd.Series(self.metadata['feature_importance'])
            
            logger.info(f"Successfully loaded model: {self.metadata['model_type']}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def calculate_metrics(self, y_true, y_pred):
        """Calculate model performance metrics."""
        metrics = {
            'precision': precision_score(y_true, y_pred),
            'recall': recall_score(y_true, y_pred),
            'f1': f1_score(y_true, y_pred)
        }
        
        # Update Prometheus metrics
        self.precision_gauge.set(metrics['precision'])
        self.recall_gauge.set(metrics['recall'])
        self.f1_gauge.set(metrics['f1'])
        
        return metrics
    
    def detect_drift(self, reference_data, current_data):
        """Detect data drift using Kolmogorov-Smirnov test."""
        try:
            # Initialize drift detector
            detector = drift.KSDrift(
                reference_data,
                p_val=0.05,
                window_size=1000
            )
            
            # Calculate drift score
            drift_score = detector.score(current_data)
            
            # Update Prometheus metric
            self.drift_score_gauge.set(drift_score)
            
            return {
                'drift_detected': drift_score > 0.05,
                'drift_score': drift_score
            }
        except Exception as e:
            logger.error(f"Error detecting drift: {str(e)}")
            return None
    
    def monitor_predictions(self, X):
        """Monitor model predictions in real-time."""
        try:
            # Get predictions
            y_pred_proba = self.model.predict_proba(X)[:, 1]
            y_pred = (y_pred_proba >= self.threshold).astype(int)
            
            # Update prediction counters
            self.prediction_counter.inc(len(y_pred))
            self.fraud_counter.inc(sum(y_pred))
            
            return y_pred, y_pred_proba
        except Exception as e:
            logger.error(f"Error making predictions: {str(e)}")
            return None, None
    
    def save_monitoring_results(self, results):
        """Save monitoring results to S3."""
        try:
            if self.s3_bucket:
                s3 = boto3.client('s3')
                
                # Add timestamp
                results['timestamp'] = datetime.now().isoformat()
                
                # Save results
                results_path = f"monitoring/results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(results_path, 'w') as f:
                    json.dump(results, f)
                
                s3.upload_file(results_path, self.s3_bucket, f"monitoring/{results_path}")
                
                logger.info(f"Saved monitoring results to S3: {results_path}")
        except Exception as e:
            logger.error(f"Error saving monitoring results: {str(e)}")

def main():
    # Start Prometheus metrics server
    start_http_server(8000)
    
    # Initialize model monitor
    monitor = ModelMonitor(
        model_path="fraud_detection_xgboost.joblib",
        metadata_path="fraud_detection_xgboost.joblib_metadata.json",
        s3_bucket="fraud-detection-models"
    )
    
    # Get current data
    current_dataset = dataiku.Dataset("current_transactions")
    current_df = current_dataset.get_dataframe()
    
    # Get reference data
    reference_dataset = dataiku.Dataset("reference_transactions")
    reference_df = reference_dataset.get_dataframe()
    
    # Monitor predictions
    y_pred, y_pred_proba = monitor.monitor_predictions(current_df)
    
    if y_pred is not None:
        # Calculate metrics if true labels are available
        if 'is_fraud' in current_df.columns:
            metrics = monitor.calculate_metrics(current_df['is_fraud'], y_pred)
        else:
            metrics = None
        
        # Detect drift
        drift_results = monitor.detect_drift(
            reference_df.drop(['is_fraud', 'customer_id', 'timestamp'], axis=1),
            current_df.drop(['customer_id', 'timestamp'], axis=1)
        )
        
        # Save monitoring results
        results = {
            'metrics': metrics,
            'drift_results': drift_results,
            'predictions_count': len(y_pred),
            'fraud_predictions_count': sum(y_pred)
        }
        
        monitor.save_monitoring_results(results)
        
        # Log results
        logger.info("Monitoring Results:")
        if metrics:
            logger.info(f"Metrics: {metrics}")
        logger.info(f"Drift Results: {drift_results}")
        logger.info(f"Total Predictions: {len(y_pred)}")
        logger.info(f"Fraud Predictions: {sum(y_pred)}")

if __name__ == "__main__":
    main() 