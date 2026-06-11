import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]
css_content = ''

os.makedirs('css', exist_ok=True)
os.makedirs('js', exist_ok=True)

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    styles = re.findall(r'<style>(.*?)</style>', content, re.DOTALL)
    if styles:
        css_content += f'\n/* From {f} */\n' + '\n'.join(styles)
    
    # Replace style tags with link tag
    content = re.sub(r'<style>.*?</style>', '<link rel="stylesheet" href="css/style.css">\n<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">', content, flags=re.DOTALL)
    
    if '</body>' in content and 'script.js' not in content:
        content = content.replace('</body>', '<script src="js/script.js"></script>\n</body>')
        
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

with open('css/style.css', 'w', encoding='utf-8') as file:
    file.write(css_content)

if not os.path.exists('js/script.js'):
    with open('js/script.js', 'w', encoding='utf-8') as file:
        file.write('// Common interactions\ndocument.addEventListener("DOMContentLoaded", () => {\n  console.log("MediCare scripts loaded");\n});\n')
