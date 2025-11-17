import markdown
from weasyprint import HTML, CSS

# Read the markdown file
with open('AXIOM_X_CLAUDE_INSTRUCTIONS_ULTIMATE.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Convert to HTML
html_content = markdown.markdown(md_content, extensions=['toc', 'tables', 'fenced_code'])

# Add styling
styled_html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>AXIOM-X Ultimate Claude Instructions</title>
    <style>
        body {
            font-family: 'Times New Roman', serif;
            margin: 40px;
            line-height: 1.6;
            font-size: 11pt;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            page-break-after: avoid;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
            page-break-after: avoid;
        }
        h3 {
            color: #7f8c8d;
            page-break-after: avoid;
        }
        code {
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        pre {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 10pt;
        }
        blockquote {
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-left: 0;
            font-style: italic;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        .check {
            color: #27ae60;
            font-weight: bold;
        }
    </style>
</head>
<body>''' + html_content + '''
</body>
</html>
'''

# Write HTML file
with open('AXIOM_X_CLAUDE_INSTRUCTIONS_ULTIMATE.html', 'w', encoding='utf-8') as f:
    f.write(styled_html)

# Convert to PDF
html_doc = HTML('AXIOM_X_CLAUDE_INSTRUCTIONS_ULTIMATE.html')
css = CSS(string='''
    @page {
        size: A4;
        margin: 1in;
    }
''')

html_doc.write_pdf('AXIOM_X_CLAUDE_INSTRUCTIONS_ULTIMATE.pdf', stylesheets=[css])
print('Ultimate Claude Instructions PDF created successfully!')