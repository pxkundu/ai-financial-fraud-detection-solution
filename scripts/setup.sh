#!/bin/bash

# Exit on error
set -e

echo "Setting up environment for AI-powered Financial Fraud Detection Solution..."

# Check for required tools
command -v aws >/dev/null 2>&1 || { echo "AWS CLI is required but not installed. Aborting." >&2; exit 1; }
command -v terraform >/dev/null 2>&1 || { echo "Terraform is required but not installed. Aborting." >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed. Aborting." >&2; exit 1; }

# Create and activate virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r application/requirements.txt
pip install -r dataiku/requirements.txt

# Install AWS CLI and configure credentials
echo "Configuring AWS credentials..."
if [ ! -f ~/.aws/credentials ]; then
    echo "AWS credentials not found. Please configure your AWS credentials:"
    aws configure
fi

# Initialize Terraform
echo "Initializing Terraform..."
terraform -chdir=infrastructure init

# Create necessary directories
echo "Creating project directories..."
mkdir -p logs
mkdir -p data/raw
mkdir -p data/processed
mkdir -p models

# Set up environment variables
echo "Setting up environment variables..."
if [ ! -f .env ]; then
    cat > .env << EOL
AWS_REGION=us-east-1
S3_BUCKET_NAME=fraud-detection-data
BEDROCK_ENDPOINT=https://bedrock.us-east-1.amazonaws.com
EKS_CLUSTER_NAME=fraud-detection-cluster
EOL
    echo "Created .env file. Please review and update the values as needed."
fi

# Set up pre-commit hooks
echo "Setting up pre-commit hooks..."
pip install pre-commit
pre-commit install

# Initialize Dataiku project
echo "Initializing Dataiku project..."
if [ -d "dataiku" ]; then
    cd dataiku
    python3 -c "import dataiku; dataiku.init_project()"
    cd ..
fi

echo "Setup completed successfully!"
echo "Please review the .env file and update the values as needed."
echo "Next steps:"
echo "1. Run './scripts/deploy.sh' to deploy the infrastructure"
echo "2. Run './scripts/monitor.sh' to start monitoring the system"
