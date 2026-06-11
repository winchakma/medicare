import os

for f in os.listdir('frontend'):
    if f.endswith('.html'):
        path = os.path.join('frontend', f)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace the incorrectly wired register button
        content = content.replace(
            '<button class="btn-primary" onclick="openAuthModal(\'login\')">Register</button>',
            '<button class="btn-primary" onclick="openAuthModal(\'register\')">Register</button>'
        )
        
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
print("Done")
