import os
import shutil
from generate_quality_visualizations import generate_quality_metrics_plot
from generate_lineage_graph import generate_lineage_graph
from generate_catalog_dashboard import generate_catalog_dashboard

def generate_and_copy_plots():
    # Create necessary directories
    os.makedirs('dataiku/plots', exist_ok=True)
    os.makedirs('docs/assets/images', exist_ok=True)
    
    # Generate all plots
    print("Generating quality metrics plot...")
    generate_quality_metrics_plot()
    
    print("Generating lineage graph...")
    generate_lineage_graph()
    
    print("Generating catalog dashboard...")
    generate_catalog_dashboard()
    
    # Copy plots to docs directory
    plot_files = [
        'quality_metrics.png',
        'lineage_graph.png',
        'catalog_dashboard.png'
    ]
    
    for plot_file in plot_files:
        source = f'dataiku/plots/{plot_file}'
        destination = f'docs/assets/images/{plot_file}'
        print(f"Copying {source} to {destination}")
        shutil.copy2(source, destination)
    
    print("All plots have been generated and copied to docs/assets/images/")

if __name__ == "__main__":
    generate_and_copy_plots() 