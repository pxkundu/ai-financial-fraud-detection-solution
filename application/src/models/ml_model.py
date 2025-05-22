import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime
import joblib
from pathlib import Path

class FraudDetectionModel:
    def __init__(self, model_path: Optional[str] = None):
        """Initialize the fraud detection model.
        
        Args:
            model_path: Optional path to a saved model file
        """
        self.model = None
        self.feature_columns = [
            'amount', 'hour', 'day_of_week', 'merchant_risk_score',
            'location_risk_score', 'customer_risk_score'
        ]
        
        if model_path and Path(model_path).exists():
            self.load_model(model_path)
        else:
            # Initialize with a simple rule-based model for testing
            self.model = self._create_rule_based_model()
    
    def _create_rule_based_model(self) -> Dict[str, Any]:
        """Create a simple rule-based model for testing."""
        return {
            'type': 'rule_based',
            'rules': {
                'high_amount_threshold': 1000.0,
                'suspicious_hours': [0, 1, 2, 3, 4, 5],  # Midnight to 5 AM
                'suspicious_merchants': ['Unknown', 'New Merchant'],
                'suspicious_locations': ['High Risk Area']
            }
        }
    
    def predict(self, features: Dict[str, Any]) -> float:
        """Predict fraud probability for a transaction.
        
        Args:
            features: Dictionary of transaction features
            
        Returns:
            float: Probability of fraud (0 to 1)
        """
        if self.model['type'] == 'rule_based':
            return self._rule_based_predict(features)
        else:
            # For ML models, convert features to array and predict
            feature_array = np.array([[features[col] for col in self.feature_columns]])
            return float(self.model.predict_proba(feature_array)[0][1])
    
    def _rule_based_predict(self, features: Dict[str, Any]) -> float:
        """Make prediction using rule-based model."""
        risk_score = 0.0
        
        # Amount-based risk
        if features['amount'] > self.model['rules']['high_amount_threshold']:
            risk_score += 0.3
        
        # Time-based risk
        hour = datetime.fromisoformat(features['timestamp']).hour
        if hour in self.model['rules']['suspicious_hours']:
            risk_score += 0.2
        
        # Merchant-based risk
        if features['merchant_name'] in self.model['rules']['suspicious_merchants']:
            risk_score += 0.3
        
        # Location-based risk
        if features['location'] in self.model['rules']['suspicious_locations']:
            risk_score += 0.2
        
        return min(risk_score, 1.0)
    
    def save_model(self, path: str) -> None:
        """Save the model to disk."""
        joblib.dump(self.model, path)
    
    def load_model(self, path: str) -> None:
        """Load a model from disk."""
        self.model = joblib.load(path)
    
    def prepare_features(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare features for prediction from raw transaction data."""
        timestamp = datetime.fromisoformat(transaction['timestamp'])
        
        return {
            'amount': float(transaction['amount']),
            'hour': timestamp.hour,
            'day_of_week': timestamp.weekday(),
            'merchant_risk_score': self._calculate_merchant_risk(transaction['merchant_name']),
            'location_risk_score': self._calculate_location_risk(transaction['location']),
            'customer_risk_score': self._calculate_customer_risk(transaction.get('customer_history', {}))
        }
    
    def _calculate_merchant_risk(self, merchant_name: str) -> float:
        """Calculate risk score for merchant."""
        if merchant_name in self.model['rules']['suspicious_merchants']:
            return 0.8
        return 0.2
    
    def _calculate_location_risk(self, location: str) -> float:
        """Calculate risk score for location."""
        if location in self.model['rules']['suspicious_locations']:
            return 0.8
        return 0.2
    
    def _calculate_customer_risk(self, customer_history: Dict[str, Any]) -> float:
        """Calculate risk score based on customer history."""
        if not customer_history:
            return 0.5
        
        risk_score = 0.0
        
        # Check for unusual transaction patterns
        if 'previous_transactions' in customer_history:
            transactions = customer_history['previous_transactions']
            if len(transactions) < 3:
                risk_score += 0.2
            
            # Check for location changes
            if customer_history.get('location_changes', 0) > 2:
                risk_score += 0.3
        
        return min(risk_score, 1.0) 