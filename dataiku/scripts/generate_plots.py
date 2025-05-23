import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np

def create_plots_directory():
    """Create plots directory if it doesn't exist."""
    plots_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    return plots_dir

def generate_sample_data():
    """Generate sample data for plotting."""
    # Create sample transaction data
    dates = pd.date_range(start='2024-01-01', end='2024-03-20', freq='D')
    transactions = pd.DataFrame({
        'date': dates,
        'amount': np.random.normal(1000, 500, len(dates)),
        'risk_score': np.random.uniform(0, 1, len(dates)),
        'is_fraud': np.random.choice([0, 1], len(dates), p=[0.95, 0.05])
    })
    return transactions

def plot_transaction_trends(data, plots_dir):
    """Plot transaction amount trends over time."""
    plt.figure(figsize=(12, 6))
    plt.plot(data['date'], data['amount'], label='Transaction Amount')
    plt.title('Transaction Amount Trends')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'transaction_trends.png'))
    plt.close()

def plot_risk_distribution(data, plots_dir):
    """Plot risk score distribution."""
    plt.figure(figsize=(10, 6))
    sns.histplot(data=data, x='risk_score', bins=30)
    plt.title('Risk Score Distribution')
    plt.xlabel('Risk Score')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'risk_distribution.png'))
    plt.close()

def plot_fraud_heatmap(data, plots_dir):
    """Plot fraud heatmap by day of week and hour."""
    data['day_of_week'] = data['date'].dt.day_name()
    data['hour'] = data['date'].dt.hour
    
    fraud_data = data[data['is_fraud'] == 1]
    pivot_table = pd.pivot_table(
        fraud_data,
        values='amount',
        index='day_of_week',
        columns='hour',
        aggfunc='count'
    )
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, cmap='YlOrRd', annot=True, fmt='.0f')
    plt.title('Fraud Incidents by Day and Hour')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'fraud_heatmap.png'))
    plt.close()

def plot_model_performance(data, plots_dir):
    """Plot model performance metrics."""
    # Simulate model performance metrics
    thresholds = np.linspace(0, 1, 100)
    precision = [0.95 - 0.5 * t for t in thresholds]
    recall = [0.8 * t for t in thresholds]
    f1_score = [2 * (p * r) / (p + r) if (p + r) > 0 else 0 
                for p, r in zip(precision, recall)]
    
    plt.figure(figsize=(10, 6))
    plt.plot(thresholds, precision, label='Precision')
    plt.plot(thresholds, recall, label='Recall')
    plt.plot(thresholds, f1_score, label='F1 Score')
    plt.title('Model Performance Metrics')
    plt.xlabel('Risk Threshold')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'model_performance.png'))
    plt.close()

def main():
    """Generate all plots."""
    plots_dir = create_plots_directory()
    data = generate_sample_data()
    
    # Generate all plots
    plot_transaction_trends(data, plots_dir)
    plot_risk_distribution(data, plots_dir)
    plot_fraud_heatmap(data, plots_dir)
    plot_model_performance(data, plots_dir)
    
    print(f"Plots generated successfully in {plots_dir}")

if __name__ == "__main__":
    main() 