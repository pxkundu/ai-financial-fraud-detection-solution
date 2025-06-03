import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

def generate_catalog_dashboard():
    # Create sample data
    datasets = [
        'raw_transactions',
        'customer_data',
        'processed_transactions',
        'feature_engineered_data',
        'model_training_data',
        'fraud_predictions'
    ]
    
    # Create DataFrame with dataset metadata
    data = {
        'Dataset': datasets,
        'Size (GB)': np.random.uniform(1, 100, len(datasets)),
        'Records': np.random.randint(1000, 1000000, len(datasets)),
        'Sensitivity': ['High', 'Medium', 'High', 'Medium', 'Low', 'High'],
        'Last Updated': pd.date_range(start='2024-01-01', periods=len(datasets), freq='D')
    }
    
    df = pd.DataFrame(data)
    
    # Create figure with subplots
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2)
    
    # 1. Dataset Size Distribution
    ax1 = fig.add_subplot(gs[0, 0])
    sns.barplot(data=df, x='Dataset', y='Size (GB)', ax=ax1)
    ax1.set_title('Dataset Size Distribution')
    ax1.tick_params(axis='x', rotation=45)
    
    # 2. Records Count
    ax2 = fig.add_subplot(gs[0, 1])
    sns.barplot(data=df, x='Dataset', y='Records', ax=ax2)
    ax2.set_title('Number of Records per Dataset')
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. Sensitivity Level Distribution
    ax3 = fig.add_subplot(gs[1, 0])
    sensitivity_counts = df['Sensitivity'].value_counts()
    ax3.pie(sensitivity_counts, labels=sensitivity_counts.index, autopct='%1.1f%%')
    ax3.set_title('Dataset Sensitivity Distribution')
    
    # 4. Last Update Timeline
    ax4 = fig.add_subplot(gs[1, 1])
    sns.scatterplot(data=df, x='Last Updated', y='Size (GB)', 
                   hue='Sensitivity', size='Records', sizes=(100, 1000),
                   ax=ax4)
    ax4.set_title('Dataset Update Timeline')
    ax4.tick_params(axis='x', rotation=45)
    
    # Adjust layout
    plt.tight_layout()
    
    # Ensure plots directory exists
    os.makedirs('dataiku/plots', exist_ok=True)
    
    # Save the plot
    plt.savefig('dataiku/plots/catalog_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    generate_catalog_dashboard() 