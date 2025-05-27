import os
from datetime import datetime

def create_initial_html():
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Financial Fraud Detection - Dataiku Module Dashboard</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            padding: 20px;
            background-color: #f5f5f5;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .content {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .card {{
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            background-color: white;
        }}
        .plot {{
            width: 100%;
            height: auto;
            margin-top: 10px;
        }}
        .test-results {{
            margin-top: 20px;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 5px;
        }}
        h1, h2, h3 {{
            color: #333;
        }}
        .timestamp {{
            color: #666;
            font-size: 0.9em;
            text-align: right;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>AI Financial Fraud Detection</h1>
        <h2>Dataiku Module Dashboard</h2>
        <p class="timestamp">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <div class="content">
        <div class="card">
            <h3>Transaction Trends</h3>
            <img src="amount_distribution.png" alt="Transaction Trends" class="plot">
        </div>
        <div class="card">
            <h3>Risk Score Distribution</h3>
            <img src="risk_scores.png" alt="Risk Distribution" class="plot">
        </div>
        <div class="card">
            <h3>Fraud Heatmap</h3>
            <img src="time_features.png" alt="Fraud Heatmap" class="plot">
        </div>
        <div class="card">
            <h3>Model Performance</h3>
            <img src="customer_statistics.png" alt="Model Performance" class="plot">
        </div>
    </div>

    <div class="test-results">
        <!-- Test results will be appended here -->
'''
    os.makedirs('../docs', exist_ok=True)
    with open('../docs/index.html', 'w') as f:
        f.write(html_content)

if __name__ == '__main__':
    create_initial_html() 