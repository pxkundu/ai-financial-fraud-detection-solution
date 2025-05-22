from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import uvicorn
from ..services.fraud_detection_service import FraudDetectionService

app = FastAPI(
    title="AI-Powered Fraud Detection API",
    description="API for detecting fraudulent transactions using ML and LLM",
    version="1.0.0"
)

# Initialize service
fraud_service = FraudDetectionService()

class Transaction(BaseModel):
    transaction_id: str
    amount: float
    merchant_name: str
    location: str
    timestamp: datetime
    customer_history: Optional[Dict] = None

class TransactionResponse(BaseModel):
    transaction_id: str
    timestamp: str
    ml_prediction: Dict
    llm_analysis: Dict
    combined_risk_score: float
    fraud_indicators: List[str]
    needs_review: bool
    recommendations: List[str]

class BatchResponse(BaseModel):
    results: List[TransactionResponse]
    batch_report: Optional[str] = None
    high_risk_count: int

@app.post("/analyze", response_model=TransactionResponse)
async def analyze_transaction(transaction: Transaction):
    """
    Analyze a single transaction for potential fraud.
    """
    try:
        result = await fraud_service.analyze_transaction(transaction.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-batch", response_model=BatchResponse)
async def analyze_batch(transactions: List[Transaction]):
    """
    Analyze multiple transactions for potential fraud.
    """
    try:
        result = await fraud_service.analyze_batch([tx.dict() for tx in transactions])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 