import os

def create_initial_html():
    html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>AI Financial Fraud Detection</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
    <style>
        body { padding: 20px; }
        .plot-container { margin: 20px 0; }
        .plot-container img { max-width: 100%; height: auto; }
        pre { background-color: #f8f9fa; padding: 15px; border-radius: 5px; }
        table { width: 100%; margin-bottom: 1rem; border-collapse: collapse; }
        th, td { padding: 0.75rem; border: 1px solid #dee2e6; }
        th { background-color: #f8f9fa; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Financial Fraud Detection</h1>
        
        <h2>Generated Plots</h2>
        <div class="row">
            <div class="col-md-12">
                <div class="plot-container">
                    <img src="amount_distribution.png" alt="Transaction amount distribution by fraud status" class="img-fluid">
                </div>
                <div class="plot-container">
                    <img src="time_features.png" alt="Time-based feature distributions" class="img-fluid">
                </div>
                <div class="plot-container">
                    <img src="risk_scores.png" alt="Risk score distributions" class="img-fluid">
                </div>
                <div class="plot-container">
                    <img src="customer_statistics.png" alt="Customer-level statistics" class="img-fluid">
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-8">
                <div id="content">'''

    os.makedirs('../docs', exist_ok=True)
    with open('../docs/index.html', 'w') as f:
        f.write(html_content)

if __name__ == '__main__':
    create_initial_html() 