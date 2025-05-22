# LLM Integration for Financial Fraud Detection

## Overview
This module enhances traditional fraud detection by integrating OpenAI's GPT models for natural language understanding and contextual analysis of transactions. It provides a hybrid approach combining machine learning predictions with LLM-powered insights.

## Features

### Transaction Analysis
- Natural language understanding of transaction descriptions
- Pattern recognition in merchant names and locations
- Contextual analysis of transaction sequences
- Anomaly detection in transaction narratives
- Risk scoring with natural language explanations

### Fraud Investigation
- Automated report generation for suspicious transactions
- Natural language explanations of fraud alerts
- Historical pattern analysis
- Risk assessment summaries
- Multi-factor analysis combining ML and LLM insights

### Customer Communication
- Automated fraud alert notifications
- Natural language responses to customer queries
- Personalized security recommendations
- Multi-language support
- Context-aware communication templates

## Implementation

### Core Components

#### OpenAI Client (`application/src/llm/openai_client.py`)
```python
class OpenAIClient:
    def __init__(self, api_key: str = None):
        # Initialize OpenAI client with API key
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-3.5-turbo"

    async def analyze_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        # Analyze transaction using GPT model
        # Returns: risk_score, fraud_indicators, recommendations

    async def generate_fraud_report(self, incidents: List[Dict[str, Any]]) -> str:
        # Generate comprehensive fraud report
        # Returns: formatted report string
```

#### Fraud Detection Service (`application/src/services/fraud_detection_service.py`)
```python
class FraudDetectionService:
    def __init__(self, risk_threshold: float = 0.7):
        # Initialize service with configurable risk threshold
        self.ml_model = FraudDetectionModel()
        self.llm_client = OpenAIClient()
        self.risk_threshold = risk_threshold

    async def analyze_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        # Combine ML and LLM analysis
        # Returns: combined_risk_score, analysis_results, needs_review

    async def analyze_batch(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Process multiple transactions concurrently
        # Returns: batch_results, high_risk_transactions, batch_report
```

## Testing

### Prerequisites
1. Set up environment variables:
```bash
# Create .env file
cp .env.example .env

# Add your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" >> .env
```

2. Install dependencies:
```bash
pip install -r application/requirements.txt
```

### Running Tests

1. Test OpenAI Integration:
```bash
# Run specific test file with verbose output
pytest application/tests/test_llm_integration.py -v

# Run with Python path set
PYTHONPATH=$PYTHONPATH:$(pwd) pytest application/tests/test_llm_integration.py -v
```

2. Test Fraud Detection with LLM:
```bash
# Run fraud detection tests
pytest application/tests/test_fraud_detection.py -v
```

### Test Cases

#### Transaction Analysis
```python
def test_transaction_analysis():
    # Test single transaction analysis
    transaction = {
        "transaction_id": "TX123456",
        "amount": 1500.00,
        "merchant_name": "Online Electronics Store",
        "location": "New York, NY",
        "timestamp": "2024-03-20T10:30:00",
        "customer_history": {
            "previous_transactions": [
                {"amount": 100.00, "merchant": "Local Grocery", "date": "2024-01-01"},
                {"amount": 50.00, "merchant": "Coffee Shop", "date": "2024-01-02"}
            ],
            "average_transaction": 75.00,
            "location_changes": 2
        }
    }
    
    # Initialize service
    service = FraudDetectionService(risk_threshold=0.7)
    
    # Get analysis results
    result = await service.analyze_transaction(transaction)
    
    # Verify results
    assert "risk_score" in result
    assert "fraud_indicators" in result
    assert "recommendations" in result
    assert 0 <= result["risk_score"] <= 1
```

#### Batch Analysis
```python
def test_batch_analysis():
    # Test multiple transactions
    transactions = [
        {
            "transaction_id": f"TX{i}",
            "amount": 100.00 * (i + 1),
            "merchant_name": f"Merchant {i}",
            "location": "New York, NY",
            "timestamp": "2024-03-20T10:30:00"
        }
        for i in range(3)
    ]
    
    # Initialize service
    service = FraudDetectionService(risk_threshold=0.7)
    
    # Get batch analysis results
    batch_result = await service.analyze_batch(transactions)
    
    # Verify results
    assert "results" in batch_result
    assert "high_risk_transactions" in batch_result
    assert "batch_report" in batch_result
```

## API Usage

### Single Transaction Analysis
```python
from application.src.services.fraud_detection_service import FraudDetectionService

# Initialize service
service = FraudDetectionService(risk_threshold=0.7)

# Analyze transaction
result = await service.analyze_transaction(transaction)
print(f"Risk Score: {result['risk_score']}")
print(f"Fraud Indicators: {result['fraud_indicators']}")
print(f"Recommendations: {result['recommendations']}")
```

### Batch Analysis
```python
# Analyze multiple transactions
batch_result = await service.analyze_batch(transactions)
print(f"High Risk Transactions: {batch_result['high_risk_transactions']}")
print(f"Batch Report: {batch_result['batch_report']}")
```

## Best Practices

### API Key Management
- Store API key in environment variables
- Use secrets management in production
- Rotate keys regularly
- Monitor API usage and costs

### Error Handling
- Implement retry logic for API calls
- Handle rate limiting gracefully
- Log errors for debugging
- Provide fallback mechanisms

### Performance Optimization
- Cache common responses
- Batch API calls when possible
- Use async/await for concurrent processing
- Monitor response times

### Security
- Validate input data
- Sanitize output
- Handle PII appropriately
- Implement rate limiting

## Troubleshooting

### Common Issues

1. API Key Errors:
```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Verify in .env file
cat .env
```

2. Rate Limiting:
```python
# Implement exponential backoff
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def analyze_with_retry(transaction):
    return await service.analyze_transaction(transaction)
```

3. Invalid Responses:
```python
# Add validation
def validate_response(response):
    assert "risk_score" in response
    assert 0 <= response["risk_score"] <= 1
    assert "fraud_indicators" in response
    assert "recommendations" in response
```

## Support

For issues related to LLM integration:
1. Check the [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
2. Review error logs in `application/logs/`
3. Open an issue in the GitHub repository
4. Contact the maintainers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## License
This module is part of the AI Financial Fraud Detection Solution and is licensed under the MIT License. 