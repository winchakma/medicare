import os

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

fa_link = '<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">'

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if fa_link not in content:
        # Insert it before </head>
        content = content.replace('</head>', f'{fa_link}\n</head>')
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)

print("FontAwesome added to all pages.")
