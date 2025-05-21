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

echo "Deploying AI-powered Financial Fraud Detection Solution..."

# Deploy infrastructure using Terraform
echo "Deploying infrastructure..."
terraform -chdir=infrastructure apply -auto-approve

# Get infrastructure outputs
echo "Getting infrastructure outputs..."
export S3_BUCKET=$(terraform -chdir=infrastructure output -raw s3_bucket_name)
export EKS_CLUSTER=$(terraform -chdir=infrastructure output -raw eks_cluster_name)
export VPC_ID=$(terraform -chdir=infrastructure output -raw vpc_id)

# Update kubeconfig
echo "Updating kubeconfig..."
aws eks update-kubeconfig --name $EKS_CLUSTER --region $AWS_REGION

# Deploy Dataiku flow
echo "Deploying Dataiku flow..."
if [ -d "dataiku" ]; then
    cd dataiku
    python3 -c "
import dataiku
import json
with open('flows/fraud_detection_flow.json', 'r') as f:
    flow = json.load(f)
dataiku.deploy_flow(flow)
"
    cd ..
fi

# Deploy monitoring stack
echo "Deploying monitoring stack..."
kubectl apply -f infrastructure/kubernetes/monitoring/

# Deploy application
echo "Deploying application..."
kubectl apply -f infrastructure/kubernetes/application/

# Wait for deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/fraud-detection-api -n fraud-detection
kubectl wait --for=condition=available --timeout=300s deployment/fraud-detection-worker -n fraud-detection

# Initialize model
echo "Initializing fraud detection model..."
python3 -c "
import dataiku
import pandas as pd
from dataiku.connector import Connector

# Get the first batch of data
dataset = dataiku.Dataset('transactions')
df = dataset.get_dataframe()

# Train initial model
from dataiku.customrecipe import get_recipe_config
config = get_recipe_config()
model = FraudDetectionModel(model_type='xgboost')
model.train(df)
model.save_model('models/fraud_detection_xgboost.joblib', s3_bucket='$S3_BUCKET')
"

# Set up CloudWatch alarms
echo "Setting up CloudWatch alarms..."
aws cloudwatch put-metric-alarm \
    --alarm-name fraud-detection-high-error-rate \
    --alarm-description "Alarm when fraud detection error rate exceeds threshold" \
    --metric-name ErrorRate \
    --namespace FraudDetection \
    --statistic Average \
    --period 300 \
    --threshold 0.05 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2 \
    --alarm-actions $(terraform -chdir=infrastructure output -raw sns_topic_arn)

# Verify deployment
echo "Verifying deployment..."
kubectl get pods -n fraud-detection
kubectl get services -n fraud-detection

echo "Deployment completed successfully!"
echo "Next steps:"
echo "1. Run './scripts/monitor.sh' to start monitoring the system"
echo "2. Check the application logs: kubectl logs -n fraud-detection deployment/fraud-detection-api"
echo "3. Access the monitoring dashboard: kubectl port-forward -n monitoring svc/grafana 3000:3000"
