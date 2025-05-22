import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve, f1_score, precision_score, recall_score
import xgboost as xgb
import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import joblib
import json
from datetime import datetime

class FraudDetectionModel:
    def __init__(self, model_type='xgboost'):
        self.model_type = model_type
        self.model = None
        self.feature_importance = None
        self.models = {
            'xgboost': xgb.XGBClassifier(
                max_depth=6,
                learning_rate=0.1,
                n_estimators=100,
                objective='binary:logistic',
                random_state=42
            ),
            'lightgbm': lgb.LGBMClassifier(
                max_depth=6,
                learning_rate=0.1,
                n_estimators=100,
                objective='binary',
                random_state=42
            ),
            'random_forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=6,
                random_state=42
            ),
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
        }
        
    def prepare_data(self, X, y):
        """Prepare data for training and testing."""
        return train_test_split(X, y, test_size=0.2, random_state=42)
    
    def train(self, X, y):
        """Train the selected model."""
        X_train, X_test, y_train, y_test = self.prepare_data(X, y)
        
        # Train model
        self.model = self.models[self.model_type]
        self.model.fit(X_train, y_train)
        
        # Get feature importance if available
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = dict(zip(X.columns, self.model.feature_importances_))
        
        return X_test, y_test
    
    def evaluate(self, X, y):
        """Evaluate model performance."""
        y_pred = self.model.predict(X)
        y_pred_proba = self.model.predict_proba(X)[:, 1]
        
        # Calculate metrics
        precision, recall, thresholds = precision_recall_curve(y, y_pred_proba)
        f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)
        optimal_idx = np.argmax(f1_scores)
        optimal_threshold = thresholds[optimal_idx]
        
        metrics = {
            'precision': precision_score(y, y_pred),
            'recall': recall_score(y, y_pred),
            'f1_score': f1_score(y, y_pred),
            'optimal_threshold': float(optimal_threshold)
        }
        
        return metrics
    
    def save_model(self, model_path):
        """Save model and metadata."""
        # Save model
        joblib.dump(self.model, model_path)
        
        # Save metadata
        metadata = {
            'model_type': self.model_type,
            'feature_importance': self.feature_importance,
            'training_date': datetime.now().isoformat(),
            'model_parameters': self.model.get_params()
        }
        
        with open(f"{model_path}_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)

if __name__ == "__main__":
    # Test the model with sample data
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
    
    # Train and evaluate model
    model = FraudDetectionModel(model_type='xgboost')
    X_test, y_test = model.train(X, y)
    metrics = model.evaluate(X_test, y_test)
    
    print("Model performance metrics:")
    print(json.dumps(metrics, indent=2))
    
    # Save model
    model.save_model('test_model.joblib')
    print("\nModel saved successfully") 