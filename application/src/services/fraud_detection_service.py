from typing import Dict, Any, List
from datetime import datetime
from ..models.ml_model import FraudDetectionModel
from ..llm.openai_client import OpenAIClient

class FraudDetectionService:
    def __init__(self, risk_threshold: float = 0.7):
        """Initialize the fraud detection service.
        
        Args:
            risk_threshold: Threshold for flagging transactions for review (0 to 1)
        """
        self.ml_model = FraudDetectionModel()
        self.llm_client = OpenAIClient()
        self.risk_threshold = risk_threshold
    
    async def analyze_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single transaction using both ML and LLM.
        
        Args:
            transaction: Dictionary containing transaction details
            
        Returns:
            Dictionary containing analysis results
        """
        # Get ML prediction
        ml_prediction = self._get_ml_prediction(transaction)
        
        # Get LLM analysis
        llm_analysis = await self.llm_client.analyze_transaction(transaction)
        
        # Combine analyses
        combined_analysis = self._combine_analyses(ml_prediction, llm_analysis)
        
        # Determine if review is needed
        needs_review = self._determine_review_needed(combined_analysis['combined_risk_score'])
        
        return {
            **combined_analysis,
            'needs_review': needs_review,
            'timestamp': datetime.now().isoformat()
        }
    
    async def analyze_batch(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze multiple transactions concurrently.
        
        Args:
            transactions: List of transaction dictionaries
            
        Returns:
            Dictionary containing batch analysis results
        """
        results = []
        high_risk_count = 0
        
        # Process each transaction
        for transaction in transactions:
            result = await self.analyze_transaction(transaction)
            results.append(result)
            
            if result['needs_review']:
                high_risk_count += 1
        
        # Generate batch report if there are high-risk transactions
        batch_report = None
        if high_risk_count > 0:
            high_risk_incidents = [
                {
                    'transaction_id': result['transaction_id'],
                    'amount': result['amount'],
                    'merchant': result['merchant_name'],
                    'risk_score': result['combined_risk_score'],
                    'fraud_indicators': result['llm_analysis']['fraud_indicators']
                }
                for result in results
                if result['needs_review']
            ]
            batch_report = await self.llm_client.generate_fraud_report(high_risk_incidents)
        
        return {
            'results': results,
            'high_risk_count': high_risk_count,
            'batch_report': batch_report,
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_ml_prediction(self, transaction: Dict[str, Any]) -> float:
        """Get ML model prediction for a transaction."""
        features = self.ml_model.prepare_features(transaction)
        return self.ml_model.predict(features)
    
    def _combine_analyses(self, ml_prediction: float, llm_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Combine ML and LLM analyses into a single result."""
        # Weight the ML prediction and LLM risk score
        ml_weight = 0.6
        llm_weight = 0.4
        
        combined_risk_score = (
            ml_weight * ml_prediction +
            llm_weight * llm_analysis['risk_score']
        )
        
        return {
            'ml_prediction': ml_prediction,
            'llm_analysis': llm_analysis,
            'combined_risk_score': combined_risk_score
        }
    
    def _determine_review_needed(self, risk_score: float) -> bool:
        """Determine if a transaction needs manual review."""
        return risk_score >= self.risk_threshold 