import os

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

old_social = """      <div class="social-links">
        <a href="#" style="font-weight:bold">FB</a>
        <a href="#" style="font-weight:bold">TW</a>
        <a href="#" style="font-weight:bold">IG</a>
      </div>"""

new_social = """      <div class="social-links">
        <a href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
        <a href="#" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
        <a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
      </div>"""

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if old_social in content:
        content = content.replace(old_social, new_social)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)

print("Replaced text social links with FontAwesome icons.")
