import markdown2
import os
import re

def update_index():
    # Read the test output markdown
    with open('tests/testOutput.md', 'r') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(md_content, extras=['tables', 'fenced-code-blocks'])
    
    # Remove the "Generated Plots" section from the markdown content
    html_content = re.sub(
        r'<h2>Generated Plots</h2>.*?<h2>Test Summary</h2>',
        '<h2>Test Summary</h2>',
        html_content,
        flags=re.DOTALL
    )
    
    # Append to index.html
    with open('../docs/index.html', 'a') as f:
        f.write('\n<h2>Feature Engineering Test Results</h2>\n')
        f.write(html_content)
        f.write('\n</div>\n</body>\n</html>')

if __name__ == '__main__':
    update_index() 