import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def generate_quality_metrics_plot():
    # Create sample data
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    metrics = {
        'Completeness': np.random.uniform(0.85, 0.99, len(dates)),
        'Consistency': np.random.uniform(0.90, 0.98, len(dates)),
        'Accuracy': np.random.uniform(0.92, 0.99, len(dates)),
        'Freshness': np.random.uniform(0.95, 1.0, len(dates))
    }
    
    df = pd.DataFrame(metrics, index=dates)
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    
    for metric in metrics.keys():
        plt.plot(df.index, df[metric], label=metric, marker='o')
    
    plt.title('Data Quality Metrics Over Time', fontsize=14, pad=20)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Quality Score', fontsize=12)
    plt.ylim(0.8, 1.0)
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    
    # Add threshold line
    plt.axhline(y=0.95, color='r', linestyle='--', alpha=0.5, label='Threshold')
    
    # Ensure plots directory exists
    os.makedirs('dataiku/plots', exist_ok=True)
    
    # Save the plot
    plt.savefig('dataiku/plots/quality_metrics.png', dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    generate_quality_metrics_plot() 