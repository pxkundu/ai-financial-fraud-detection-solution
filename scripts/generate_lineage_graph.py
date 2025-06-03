import networkx as nx
import matplotlib.pyplot as plt
import os

def generate_lineage_graph():
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add nodes (datasets)
    datasets = [
        'raw_transactions',
        'customer_data',
        'processed_transactions',
        'feature_engineered_data',
        'model_training_data',
        'fraud_predictions'
    ]
    
    # Add edges (transformations)
    edges = [
        ('raw_transactions', 'processed_transactions'),
        ('customer_data', 'processed_transactions'),
        ('processed_transactions', 'feature_engineered_data'),
        ('feature_engineered_data', 'model_training_data'),
        ('model_training_data', 'fraud_predictions')
    ]
    
    # Add nodes and edges to the graph
    G.add_nodes_from(datasets)
    G.add_edges_from(edges)
    
    # Set up the plot
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=1, iterations=50)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, 
                          node_color='lightblue',
                          node_size=2000,
                          alpha=0.7)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos,
                          edge_color='gray',
                          arrows=True,
                          arrowsize=20,
                          width=2,
                          alpha=0.6)
    
    # Add labels
    nx.draw_networkx_labels(G, pos,
                           font_size=10,
                           font_weight='bold')
    
    # Add edge labels
    edge_labels = {
        ('raw_transactions', 'processed_transactions'): 'Clean & Transform',
        ('customer_data', 'processed_transactions'): 'Join',
        ('processed_transactions', 'feature_engineered_data'): 'Feature Engineering',
        ('feature_engineered_data', 'model_training_data'): 'Split & Prepare',
        ('model_training_data', 'fraud_predictions'): 'Model Prediction'
    }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title('Data Lineage Graph', fontsize=14, pad=20)
    plt.axis('off')
    
    # Ensure plots directory exists
    os.makedirs('dataiku/plots', exist_ok=True)
    
    # Save the plot
    plt.savefig('dataiku/plots/lineage_graph.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    generate_lineage_graph() 