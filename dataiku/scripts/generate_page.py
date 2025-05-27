import markdown2
import os

def generate_html_page():
    # Read the test output markdown
    with open('tests/testOutput.md', 'r') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(md_content, extras=['tables', 'fenced-code-blocks'])
    
    # Create the HTML page
    html = f'''<!DOCTYPE html>
<html>
<head>
    <title>Dataiku Test Results</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
    <style>
        body {{ padding: 20px; }}
        .plot-container {{ margin: 20px 0; }}
        .plot-container img {{ max-width: 100%; height: auto; }}
        pre {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; }}
        table {{ width: 100%; margin-bottom: 1rem; border-collapse: collapse; }}
        th, td {{ padding: 0.75rem; border: 1px solid #dee2e6; }}
        th {{ background-color: #f8f9fa; }}
        .container {{ max-width: 1400px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="mb-4">Dataiku Test Results</h1>
        <div class="row">
            <div class="col-md-8">
                {html_content}
            </div>
            <div class="col-md-4">
                <h3>Generated Plots</h3>
                <div class="plot-container">
                    <h4>Amount Distribution</h4>
                    <img src="amount_distribution.png" alt="Amount Distribution">
                </div>
                <div class="plot-container">
                    <h4>Time Features</h4>
                    <img src="time_features.png" alt="Time Features">
                </div>
                <div class="plot-container">
                    <h4>Risk Scores</h4>
                    <img src="risk_scores.png" alt="Risk Scores">
                </div>
                <div class="plot-container">
                    <h4>Customer Statistics</h4>
                    <img src="customer_statistics.png" alt="Customer Statistics">
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    # Create docs directory if it doesn't exist
    os.makedirs('docs/dataiku', exist_ok=True)
    
    # Write the HTML file
    with open('docs/dataiku/index.html', 'w') as f:
        f.write(html)

if __name__ == '__main__':
    generate_html_page() 