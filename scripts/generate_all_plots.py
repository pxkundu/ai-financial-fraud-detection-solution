#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def create_directory(path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)

def generate_quality_metrics():
    """Generate quality metrics visualization."""
    # Create sample data
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    metrics = {
        'Completeness': np.random.normal(0.95, 0.02, len(dates)),
        'Consistency': np.random.normal(0.92, 0.03, len(dates)),
        'Accuracy': np.random.normal(0.94, 0.02, len(dates)),
        'Freshness': np.random.normal(0.98, 0.01, len(dates))
    }
    
    df = pd.DataFrame(metrics, index=dates)
    
    # Create plot
    plt.figure(figsize=(12, 6))
    for column in df.columns:
        plt.plot(df.index, df[column], label=column, marker='o')
    
    plt.title('Data Quality Metrics Over Time')
    plt.xlabel('Date')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save plot
    plt.savefig('docs/assets/images/quality_metrics.png')
    plt.close()

def generate_lineage_graph():
    """Generate data lineage visualization."""
    # Create sample data
    nodes = ['Raw Data', 'Cleaned Data', 'Features', 'Model Input', 'Predictions']
    edges = [
        ('Raw Data', 'Cleaned Data'),
        ('Cleaned Data', 'Features'),
        ('Features', 'Model Input'),
        ('Model Input', 'Predictions')
    ]
    
    # Create plot
    plt.figure(figsize=(10, 6))
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=2000, arrowsize=20, font_size=10)
    
    plt.title('Data Lineage Graph')
    plt.tight_layout()
    
    # Save plot
    plt.savefig('docs/assets/images/lineage_graph.png')
    plt.close()

def generate_catalog_dashboard():
    """Generate data catalog visualization."""
    # Create sample data
    datasets = ['Transactions', 'Customers', 'Products', 'Fraud Cases']
    metrics = {
        'Size (GB)': [100, 50, 30, 20],
        'Records (M)': [10, 5, 3, 2],
        'Sensitivity': ['High', 'High', 'Medium', 'High'],
        'Update Freq': ['Real-time', 'Daily', 'Weekly', 'Real-time']
    }
    
    df = pd.DataFrame(metrics, index=datasets)
    
    # Create plot
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Size plot
    df['Size (GB)'].plot(kind='bar', ax=axes[0,0])
    axes[0,0].set_title('Dataset Sizes')
    axes[0,0].set_ylabel('Size (GB)')
    
    # Records plot
    df['Records (M)'].plot(kind='bar', ax=axes[0,1])
    axes[0,1].set_title('Record Counts')
    axes[0,1].set_ylabel('Records (M)')
    
    # Sensitivity plot
    sensitivity_counts = df['Sensitivity'].value_counts()
    sensitivity_counts.plot(kind='pie', ax=axes[1,0])
    axes[1,0].set_title('Data Sensitivity Distribution')
    
    # Update frequency plot
    update_counts = df['Update Freq'].value_counts()
    update_counts.plot(kind='pie', ax=axes[1,1])
    axes[1,1].set_title('Update Frequency Distribution')
    
    plt.tight_layout()
    
    # Save plot
    plt.savefig('docs/assets/images/catalog_dashboard.png')
    plt.close()

def generate_pipeline_metrics():
    """Generate pipeline performance metrics."""
    # Create sample data
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    metrics = {
        'Processing Time': np.random.normal(100, 10, len(dates)),
        'Success Rate': np.random.normal(0.98, 0.01, len(dates)),
        'Data Volume': np.random.normal(1000000, 100000, len(dates)),
        'Error Rate': np.random.normal(0.02, 0.005, len(dates))
    }
    
    df = pd.DataFrame(metrics, index=dates)
    
    # Create plot
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Processing time plot
    df['Processing Time'].plot(ax=axes[0,0])
    axes[0,0].set_title('Average Processing Time')
    axes[0,0].set_ylabel('Seconds')
    
    # Success rate plot
    df['Success Rate'].plot(ax=axes[0,1])
    axes[0,1].set_title('Pipeline Success Rate')
    axes[0,1].set_ylabel('Rate')
    
    # Data volume plot
    df['Data Volume'].plot(ax=axes[1,0])
    axes[1,0].set_title('Daily Data Volume')
    axes[1,0].set_ylabel('Records')
    
    # Error rate plot
    df['Error Rate'].plot(ax=axes[1,1])
    axes[1,1].set_title('Error Rate')
    axes[1,1].set_ylabel('Rate')
    
    plt.tight_layout()
    
    # Save plot
    plt.savefig('docs/assets/images/pipeline_metrics.png')
    plt.close()

def main():
    """Generate all visualizations."""
    # Create necessary directories
    create_directory('docs/assets/images')
    
    # Generate visualizations
    generate_quality_metrics()
    generate_lineage_graph()
    generate_catalog_dashboard()
    generate_pipeline_metrics()
    
    print("All visualizations have been generated successfully!")

if __name__ == "__main__":
    main() 