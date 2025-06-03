from generate_quality_visualizations import generate_quality_metrics_plot
from generate_lineage_graph import generate_lineage_graph
from generate_catalog_dashboard import generate_catalog_dashboard
import os

def generate_all_plots():
    # Ensure plots directory exists
    os.makedirs('dataiku/plots', exist_ok=True)
    
    # Generate all plots
    print("Generating quality metrics plot...")
    generate_quality_metrics_plot()
    
    print("Generating lineage graph...")
    generate_lineage_graph()
    
    print("Generating catalog dashboard...")
    generate_catalog_dashboard()
    
    print("\nAll plots have been generated successfully!")
    print("Plots are saved in: dataiku/plots/")

if __name__ == "__main__":
    generate_all_plots() 