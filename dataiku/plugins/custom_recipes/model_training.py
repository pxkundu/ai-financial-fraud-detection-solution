import dataiku
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import precision_recall_curve, average_precision_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import xgboost as xgb
import lightgbm as lgb
import joblib
import boto3
import json
from datetime import datetime

class FraudDetectionModel:
    def __init__(self, model_type='xgboost'):
        self.model_type = model_type
        self.models = {
            'xgboost': xgb.XGBClassifier(
                max_depth=6,
                learning_rate=0.1,
                n_estimators=100,
                objective='binary:logistic',
                scale_pos_weight=10
            ),
            'lightgbm': lgb.LGBMClassifier(
                num_leaves=31,
                learning_rate=0.1,
                n_estimators=100,
                class_weight='balanced'
            ),
            'random_forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                class_weight='balanced'
            ),
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=6
            )
        }
        self.model = self.models[model_type]
        self.feature_importance = None
        self.threshold = None

    def prepare_data(self, df):
        """Prepare data for training."""
        # Separate features and target
        X = df.drop(['is_fraud', 'customer_id', 'timestamp'], axis=1)
        y = df['is_fraud']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        return X_train, X_test, y_train, y_test, X.columns

    def train(self, X_train, y_train):
        """Train the model."""
        self.model.fit(X_train, y_train)
        
        # Get feature importance
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.Series(
                self.model.feature_importances_,
                index=X_train.columns
            ).sort_values(ascending=False)

    def evaluate(self, X_test, y_test):
        """Evaluate model performance."""
        # Get predictions
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Calculate precision-recall curve
        precision, recall, thresholds = precision_recall_curve(y_test, y_pred_proba)
        
        # Find optimal threshold
        f1_scores = 2 * (precision * recall) / (precision + recall)
        optimal_idx = np.argmax(f1_scores)
        self.threshold = thresholds[optimal_idx]
        
        # Calculate metrics
        y_pred = (y_pred_proba >= self.threshold).astype(int)
        metrics = {
            'average_precision': average_precision_score(y_test, y_pred_proba),
            'optimal_threshold': float(self.threshold),
            'f1_score': float(f1_scores[optimal_idx])
        }
        
        return metrics

    def save_model(self, model_path, s3_bucket=None):
        """Save model to local path or S3."""
        # Save model locally
        joblib.dump(self.model, model_path)
        
        # Save metadata
        metadata = {
            'model_type': self.model_type,
            'threshold': self.threshold,
            'feature_importance': self.feature_importance.to_dict(),
            'timestamp': datetime.now().isoformat()
        }
        
        with open(f"{model_path}_metadata.json", 'w') as f:
            json.dump(metadata, f)
        
        # Upload to S3 if bucket specified
        if s3_bucket:
            s3 = boto3.client('s3')
            s3.upload_file(model_path, s3_bucket, f"models/{model_path}")
            s3.upload_file(
                f"{model_path}_metadata.json",
                s3_bucket,
                f"models/{model_path}_metadata.json"
            )

def main():
    # Get processed dataset
    input_dataset = dataiku.Dataset("processed_transactions")
    df = input_dataset.get_dataframe()
    
    # Initialize and train models
    models = {}
    metrics = {}
    
    for model_type in ['xgboost', 'lightgbm', 'random_forest', 'gradient_boosting']:
        print(f"Training {model_type} model...")
        
        # Initialize model
        model = FraudDetectionModel(model_type=model_type)
        
        # Prepare data
        X_train, X_test, y_train, y_test, feature_names = model.prepare_data(df)
        
        # Train model
        model.train(X_train, y_train)
        
        # Evaluate model
        model_metrics = model.evaluate(X_test, y_test)
        
        # Save model
        model_path = f"fraud_detection_{model_type}.joblib"
        model.save_model(model_path, s3_bucket="fraud-detection-models")
        
        models[model_type] = model
        metrics[model_type] = model_metrics
    
    # Select best model
    best_model_type = max(metrics, key=lambda x: metrics[x]['f1_score'])
    best_model = models[best_model_type]
    
    print(f"Best model: {best_model_type}")
    print(f"F1 Score: {metrics[best_model_type]['f1_score']:.4f}")
    print(f"Average Precision: {metrics[best_model_type]['average_precision']:.4f}")
    
    # Save model comparison results
    comparison_df = pd.DataFrame(metrics).T
    output_dataset = dataiku.Dataset("model_comparison")
    output_dataset.write_with_schema(comparison_df)

if __name__ == "__main__":
    main() 