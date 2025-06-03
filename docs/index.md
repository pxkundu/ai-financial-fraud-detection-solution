---
layout: default
title: AI Financial Fraud Detection - Data Quality and Governance
---

# Data Quality and Governance Visualizations

## Quality Metrics Dashboard
![Quality Metrics Dashboard](../assets/images/quality_metrics.png)
*Daily tracking of data quality metrics including completeness, consistency, accuracy, and freshness*

## Data Lineage Graph
![Data Lineage Graph](../assets/images/lineage_graph.png)
*Visual representation of data flow and transformations across the pipeline*

## Data Catalog Dashboard
![Data Catalog Dashboard](../assets/images/catalog_dashboard.png)
*Comprehensive view of dataset metadata, including size, records, sensitivity, and update frequency*

## How to Update Visualizations

To update these visualizations:

1. Run the plot generation script:
```bash
python scripts/generate_all_plots.py
```

2. Commit and push the changes:
```bash
git add docs/assets/images/
git commit -m "Update data quality and governance visualizations"
git push
```

The GitHub Pages site will automatically update with the new visualizations. 