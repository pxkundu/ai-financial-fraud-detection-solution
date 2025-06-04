import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def create_directory(path):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def generate_model_metrics():
    """Generate model performance metrics visualization."""
    metrics = {
        'Model': ['Model A', 'Model B', 'Model C', 'Model D'],
        'Accuracy': [0.992, 0.985, 0.978, 0.972],
        'Precision': [0.985, 0.978, 0.972, 0.965],
        'Recall': [0.978, 0.972, 0.965, 0.958],
        'F1 Score': [0.981, 0.975, 0.968, 0.961]
    }
    
    df = pd.DataFrame(metrics)
    df_melted = pd.melt(df, id_vars=['Model'], 
                        value_vars=['Accuracy', 'Precision', 'Recall', 'F1 Score'],
                        var_name='Metric', value_name='Score')
    
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    sns.barplot(data=df_melted, x='Model', y='Score', hue='Metric')
    plt.title('Model Performance Metrics', fontsize=14, pad=20)
    plt.xlabel('Model Version', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.ylim(0.9, 1.0)
    plt.legend(title='Metrics', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    create_directory('docs/assets/images')
    plt.savefig('docs/assets/images/model_metrics.png', dpi=300, bbox_inches='tight')
    plt.close()


def generate_system_metrics():
    """Generate system performance metrics visualization."""
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    metrics = {
        'Latency (ms)': np.random.normal(150, 10, len(dates)),
        'Throughput (TPS)': np.random.normal(10000, 500, len(dates)),
        'CPU Usage (%)': np.random.normal(65, 5, len(dates)),
        'Memory Usage (%)': np.random.normal(70, 5, len(dates))
    }
    
    df = pd.DataFrame(metrics, index=dates)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('System Performance Metrics', fontsize=16, y=1.02)
    
    for (metric, data), ax in zip(metrics.items(), axes.ravel()):
        sns.lineplot(data=df, x=df.index, y=metric, ax=ax)
        ax.set_title(metric)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    create_directory('docs/assets/images')
    plt.savefig('docs/assets/images/system_metrics.png', dpi=300, bbox_inches='tight')
    plt.close()


def generate_quality_metrics():
    """Generate data quality metrics visualization."""
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    metrics = {
        'Completeness': np.random.uniform(0.985, 0.995, len(dates)),
        'Consistency': np.random.uniform(0.978, 0.988, len(dates)),
        'Accuracy': np.random.uniform(0.982, 0.992, len(dates)),
        'Freshness': np.random.uniform(0.989, 0.999, len(dates))
    }
    
    df = pd.DataFrame(metrics, index=dates)
    
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    
    for metric in metrics.keys():
        plt.plot(df.index, df[metric], label=metric, marker='o')
    
    plt.title('Data Quality Metrics Over Time', fontsize=14, pad=20)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Quality Score', fontsize=12)
    plt.ylim(0.97, 1.0)
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    
    plt.axhline(y=0.98, color='r', linestyle='--', alpha=0.5, label='Threshold')
    
    create_directory('docs/assets/images')
    plt.savefig('docs/assets/images/quality_metrics.png', dpi=300, bbox_inches='tight')
    plt.close()


def main():
    """Generate all portfolio visualizations."""
    print("Generating portfolio visualizations...")
    generate_model_metrics()
    generate_system_metrics()
    generate_quality_metrics()
    print("All visualizations generated successfully!")


if __name__ == "__main__":
    main() 