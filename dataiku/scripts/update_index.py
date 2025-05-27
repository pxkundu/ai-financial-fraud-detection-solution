import markdown2
import os
import re

def update_index():
    # Read the test output markdown
    with open('tests/testOutput.md', 'r') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(md_content, extras=['tables', 'fenced-code-blocks'])
    
    # Fix image paths to be relative to the deployed site
    html_content = re.sub(
        r'src="dataiku/plots/([^"]+)"',
        r'src="\1"',
        html_content
    )
    
    # Append to index.html
    with open('../docs/index.html', 'a') as f:
        f.write('\n\n## Feature Engineering Test Results\n\n')
        f.write(html_content)
        f.write('\n</div></div></div></body></html>')

if __name__ == '__main__':
    update_index() 