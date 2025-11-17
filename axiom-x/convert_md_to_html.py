import markdown
from weasyprint import HTML, CSS

# Read the markdown file
with open('AXIOM_X_USERS_GUIDE.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Convert to HTML
html_content = markdown.markdown(md_content, extensions=['toc', 'tables', 'fenced_code'])

# Add styling with proper text wrapping
styled_html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Axiom-X User Guide</title>
    <style>
        body {
            font-family: 'Times New Roman', serif;
            margin: 40px;
            line-height: 1.6;
            font-size: 11pt;
            word-wrap: break-word;
            overflow-wrap: break-word;
            hyphens: auto;
            text-align: justify;
            max-width: none;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            page-break-after: avoid;
            word-wrap: break-word;
            hyphens: auto;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
            page-break-after: avoid;
            word-wrap: break-word;
            hyphens: auto;
        }
        h3 {
            color: #7f8c8d;
            word-wrap: break-word;
            hyphens: auto;
        }
        p {
            margin: 10px 0;
            text-align: justify;
            word-wrap: break-word;
            overflow-wrap: break-word;
            hyphens: auto;
        }
        li {
            margin: 5px 0;
            word-wrap: break-word;
            overflow-wrap: break-word;
            hyphens: auto;
        }
        code {
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            word-wrap: break-word;
            white-space: pre-wrap;
            font-size: 10pt;
        }
        pre {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        blockquote {
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-left: 0;
            font-style: italic;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
            table-layout: auto;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
            word-wrap: break-word;
            overflow-wrap: break-word;
            hyphens: auto;
        }
        th {
            background-color: #f2f2f2;
        }
        .check {
            color: #27ae60;
            font-weight: bold;
        }
        /* Ensure all text elements wrap properly */
        * {
            box-sizing: border-box;
        }
        div, span, section {
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
    </style>
</head>
<body>''' + html_content + '''
</body>
</html>
'''

# Write HTML file
with open('AXIOM_X_USERS_GUIDE.html', 'w', encoding='utf-8') as f:
    f.write(styled_html)

# Convert to PDF with proper page settings
html_doc = HTML('AXIOM_X_USERS_GUIDE.html')
css = CSS(string='''
    @page {
        size: A4;
        margin: 1in;
    }
    body {
        word-wrap: break-word;
        overflow-wrap: break-word;
        hyphens: auto;
    }
    * {
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
''')

html_doc.write_pdf('AXIOM_X_USERS_GUIDE.pdf', stylesheets=[css])
print('User Guide PDF created successfully with proper text wrapping!')