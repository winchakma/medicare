import os

for f in os.listdir('frontend'):
    if f.endswith('.html'):
        path = os.path.join('frontend', f)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        content = content.replace('href="css/style.css"', 'href="css/style.css?v=2"')
        content = content.replace('src="js/script.js"', 'src="js/script.js?v=2"')
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
