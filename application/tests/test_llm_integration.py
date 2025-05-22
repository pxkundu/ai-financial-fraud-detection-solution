import pytest
import os
from datetime import datetime
from application.src.llm.openai_client import OpenAIClient
from application.src.services.fraud_detection_service import FraudDetectionService

@pytest.fixture
def openai_client():
    return OpenAIClient()

@pytest.fixture
def fraud_service():
    return FraudDetectionService()

@pytest.fixture
def sample_transaction():
    return {
        "transaction_id": "TX123456",
        "amount": 1500.00,
        "merchant_name": "Online Electronics Store",
        "location": "New York, NY",
        "timestamp": datetime.now().isoformat(),
        "customer_history": {
            "previous_transactions": [
                {"amount": 100.00, "merchant": "Local Grocery", "date": "2024-01-01"},
                {"amount": 50.00, "merchant": "Coffee Shop", "date": "2024-01-02"}
            ],
            "average_transaction": 75.00,
            "location_changes": 2
        }
    }

@pytest.mark.asyncio
async def test_transaction_analysis(openai_client, sample_transaction):
    """Test transaction analysis with OpenAI."""
    result = await openai_client.analyze_transaction(sample_transaction)
    
    assert "raw_analysis" in result
    assert "risk_score" in result
    assert "fraud_indicators" in result
    assert "recommendations" in result
    
    # Verify risk score is between 0 and 1
    assert 0 <= result["risk_score"] <= 1

@pytest.mark.asyncio
async def test_fraud_report_generation(openai_client):
    """Test fraud report generation with OpenAI."""
    incidents = [
        {
            "transaction_id": "TX123456",
            "amount": 1500.00,
            "merchant": "Online Electronics",
            "risk_score": 0.85,
            "fraud_indicators": ["Unusual amount", "New merchant"]
        },
        {
            "transaction_id": "TX123457",
            "amount": 2000.00,
            "merchant": "Unknown Store",
            "risk_score": 0.92,
            "fraud_indicators": ["High amount", "Unknown merchant"]
        }
    ]
    
    report = await openai_client.generate_fraud_report(incidents)
    assert isinstance(report, str)
    assert len(report) > 0

@pytest.mark.asyncio
async def test_combined_analysis(fraud_service, sample_transaction):
    """Test combined ML and LLM analysis."""
    result = await fraud_service.analyze_transaction(sample_transaction)
    
    assert "ml_prediction" in result
    assert "llm_analysis" in result
    assert "combined_risk_score" in result
    assert "needs_review" in result
    
    # Verify combined risk score is between 0 and 1
    assert 0 <= result["combined_risk_score"] <= 1

@pytest.mark.asyncio
async def test_batch_analysis(fraud_service):
    """Test batch transaction analysis."""
    transactions = [
        {
            "transaction_id": f"TX{i}",
            "amount": 100.00 * (i + 1),
            "merchant_name": f"Merchant {i}",
            "location": "New York, NY",
            "timestamp": datetime.now().isoformat()
        }
        for i in range(3)
    ]
    
    result = await fraud_service.analyze_batch(transactions)
    
    assert "results" in result
    assert "high_risk_count" in result
    assert len(result["results"]) == len(transactions)
    
    # If any high-risk transactions, should have a batch report
    if result["high_risk_count"] > 0:
        assert "batch_report" in result
        assert isinstance(result["batch_report"], str) 