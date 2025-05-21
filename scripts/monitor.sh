#!/bin/bash

# Exit on error
set -e

# Load environment variables
if [ -f .env ]; then
    source .env
else
    echo "Error: .env file not found. Please run setup.sh first."
    exit 1
fi

echo "Starting monitoring for AI-powered Financial Fraud Detection Solution..."

# Function to check CloudWatch logs
check_cloudwatch_logs() {
    echo "Checking CloudWatch logs..."
    aws logs describe-log-groups --region $AWS_REGION | grep fraud-detection
    
    # Get recent log events
    aws logs get-log-events \
        --log-group-name /fraud-detection/application \
        --log-stream-name $(aws logs describe-log-streams \
            --log-group-name /fraud-detection/application \
            --order-by LastEventTime \
            --descending \
            --limit 1 \
            --query 'logStreams[0].logStreamName' \
            --output text) \
        --limit 10
}

# Function to check system metrics
check_system_metrics() {
    echo "Checking system metrics..."
    
    # Check EKS cluster status
    echo "EKS Cluster Status:"
    aws eks describe-cluster --name $EKS_CLUSTER --region $AWS_REGION \
        --query 'cluster.status' --output text
    
    # Check pod status
    echo "Pod Status:"
    kubectl get pods -n fraud-detection
    
    # Check Dataiku flow status
    echo "Dataiku Flow Status:"
    if [ -d "dataiku" ]; then
        cd dataiku
        python3 -c "
import dataiku
flow = dataiku.get_flow('fraud_detection_flow')
print(f'Flow Status: {flow.get_status()}')
"
        cd ..
    fi
}

# Function to check model performance
check_model_performance() {
    echo "Checking model performance..."
    
    # Get latest model metrics from S3
    aws s3 cp s3://$S3_BUCKET/monitoring/latest_metrics.json - 2>/dev/null || echo "No metrics found"
    
    # Check model drift
    echo "Checking for model drift..."
    python3 -c "
import dataiku
import pandas as pd
from dataiku.customrecipe import get_recipe_config

# Get current and reference data
current_data = dataiku.Dataset('current_transactions').get_dataframe()
reference_data = dataiku.Dataset('reference_transactions').get_dataframe()

# Check for drift
from alibi_detect import drift
detector = drift.KSDrift(reference_data, p_val=0.05)
drift_score = detector.score(current_data)
print(f'Drift Score: {drift_score}')
"
}

# Function to check alerts
check_alerts() {
    echo "Checking CloudWatch alarms..."
    aws cloudwatch describe-alarms \
        --alarm-name-prefix fraud-detection \
        --state-value ALARM \
        --region $AWS_REGION
}

# Function to start monitoring dashboard
start_monitoring_dashboard() {
    echo "Starting monitoring dashboard..."
    
    # Start Grafana port-forward in background
    kubectl port-forward -n monitoring svc/grafana 3000:3000 &
    GRAFANA_PID=$!
    
    # Start Prometheus port-forward in background
    kubectl port-forward -n monitoring svc/prometheus-server 9090:9090 &
    PROMETHEUS_PID=$!
    
    echo "Monitoring dashboards available at:"
    echo "Grafana: http://localhost:3000"
    echo "Prometheus: http://localhost:9090"
    
    # Wait for user input to stop
    read -p "Press Enter to stop monitoring..."
    
    # Cleanup
    kill $GRAFANA_PID $PROMETHEUS_PID
}

# Main monitoring loop
while true; do
    echo "=== Monitoring Report ==="
    echo "Timestamp: $(date)"
    
    check_cloudwatch_logs
    check_system_metrics
    check_model_performance
    check_alerts
    
    echo "=== End of Report ==="
    echo ""
    
    # Ask user if they want to start the monitoring dashboard
    read -p "Start monitoring dashboard? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        start_monitoring_dashboard
    fi
    
    # Wait for 5 minutes before next check
    echo "Waiting 5 minutes before next check..."
    sleep 300
done
