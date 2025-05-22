import os
from typing import Dict, Any, List
import openai
from datetime import datetime

class OpenAIClient:
    def __init__(self):
        """Initialize the OpenAI client."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        openai.api_key = self.api_key
    
    async def analyze_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a transaction using OpenAI's API.
        
        Args:
            transaction: Dictionary containing transaction details
            
        Returns:
            Dictionary containing analysis results
        """
        prompt = self._create_analysis_prompt(transaction)
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a fraud detection expert analyzing financial transactions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "raw_analysis": analysis,
                "risk_score": self._extract_risk_score(analysis),
                "fraud_indicators": self._extract_fraud_indicators(analysis),
                "recommendations": self._extract_recommendations(analysis)
            }
            
        except Exception as e:
            print(f"Error in OpenAI API call: {str(e)}")
            return {
                "raw_analysis": "Error in analysis",
                "risk_score": 0.5,
                "fraud_indicators": ["API Error"],
                "recommendations": ["Please try again later"]
            }
    
    async def generate_fraud_report(self, incidents: List[Dict[str, Any]]) -> str:
        """Generate a fraud report for multiple incidents.
        
        Args:
            incidents: List of fraud incidents
            
        Returns:
            String containing the generated report
        """
        prompt = self._create_report_prompt(incidents)
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a fraud detection expert generating incident reports."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error in OpenAI API call: {str(e)}")
            return "Error generating fraud report"
    
    def _create_analysis_prompt(self, transaction: Dict[str, Any]) -> str:
        """Create a prompt for transaction analysis."""
        return f"""
        Analyze the following transaction for potential fraud:
        
        Transaction ID: {transaction['transaction_id']}
        Amount: ${transaction['amount']}
        Merchant: {transaction['merchant_name']}
        Location: {transaction['location']}
        Timestamp: {transaction['timestamp']}
        
        Customer History:
        {self._format_customer_history(transaction.get('customer_history', {}))}
        
        Please provide:
        1. A risk score between 0 and 1
        2. List of potential fraud indicators
        3. Recommendations for further action
        """
    
    def _create_report_prompt(self, incidents: List[Dict[str, Any]]) -> str:
        """Create a prompt for fraud report generation."""
        incidents_text = "\n\n".join([
            f"Incident {i+1}:\n" +
            f"Transaction ID: {inc['transaction_id']}\n" +
            f"Amount: ${inc['amount']}\n" +
            f"Merchant: {inc['merchant']}\n" +
            f"Risk Score: {inc['risk_score']}\n" +
            f"Fraud Indicators: {', '.join(inc['fraud_indicators'])}"
            for i, inc in enumerate(incidents)
        ])
        
        return f"""
        Generate a comprehensive fraud report for the following incidents:
        
        {incidents_text}
        
        Please include:
        1. Summary of incidents
        2. Common patterns and trends
        3. Risk assessment
        4. Recommended actions
        """
    
    def _format_customer_history(self, history: Dict[str, Any]) -> str:
        """Format customer history for the prompt."""
        if not history:
            return "No customer history available"
        
        text = []
        if 'previous_transactions' in history:
            text.append("Previous Transactions:")
            for tx in history['previous_transactions']:
                text.append(f"- ${tx['amount']} at {tx['merchant']} on {tx['date']}")
        
        if 'average_transaction' in history:
            text.append(f"Average Transaction: ${history['average_transaction']}")
        
        if 'location_changes' in history:
            text.append(f"Location Changes: {history['location_changes']}")
        
        return "\n".join(text)
    
    def _extract_risk_score(self, analysis: str) -> float:
        """Extract risk score from analysis text."""
        try:
            # Look for risk score in the format "risk score: X" or "risk: X"
            import re
            match = re.search(r'risk\s*score:?\s*(\d*\.?\d+)', analysis.lower())
            if match:
                score = float(match.group(1))
                return min(max(score, 0.0), 1.0)
        except:
            pass
        return 0.5  # Default to medium risk if extraction fails
    
    def _extract_fraud_indicators(self, analysis: str) -> List[str]:
        """Extract fraud indicators from analysis text."""
        indicators = []
        try:
            # Look for indicators in the format "indicators:" or "fraud indicators:"
            import re
            match = re.search(r'(?:fraud\s*)?indicators:?\s*(.*?)(?:\n\n|\Z)', analysis, re.DOTALL | re.IGNORECASE)
            if match:
                indicators_text = match.group(1)
                indicators = [ind.strip() for ind in indicators_text.split('\n') if ind.strip()]
        except:
            pass
        return indicators or ["Unable to extract indicators"]
    
    def _extract_recommendations(self, analysis: str) -> List[str]:
        """Extract recommendations from analysis text."""
        recommendations = []
        try:
            # Look for recommendations in the format "recommendations:" or "recommended actions:"
            import re
            match = re.search(r'(?:recommended\s*)?(?:actions|recommendations):?\s*(.*?)(?:\n\n|\Z)', analysis, re.DOTALL | re.IGNORECASE)
            if match:
                recs_text = match.group(1)
                recommendations = [rec.strip() for rec in recs_text.split('\n') if rec.strip()]
        except:
            pass
        return recommendations or ["Unable to extract recommendations"] 