import re

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Remove ALL body, *, and :root declarations from the raw concatenated CSS
css = re.sub(r'\*,\s*\*\:\:before,\s*\*\:\:after\s*\{[^}]+\}', '', css)
css = re.sub(r':root\s*\{[^}]+\}', '', css)
css = re.sub(r'body\s*\{[^}]+\}', '', css)

# 2. Add back a single unified reset and global vars
global_css = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --navy: #0A1628; --teal: #0D9B76; --teal-light: #E1F5EE; --teal-mid: #1D9E75; --white: #ffffff;
  --gray-50: #F8F9FB; --gray-100: #EFF1F5; --gray-200: #D8DCE6;
  --gray-500: #6B7280; --gray-700: #374151; --gray-900: #111827;
  --coral: #F0997B; --amber: #EF9F27; --red: #EF4444; --green: #22c55e;
  --sidebar: #0A1628;
}
body { font-family: 'Inter', sans-serif; color: var(--gray-900); background: var(--gray-50); }
a { text-decoration: none; color: inherit; }
body.admin-body { display: flex; min-height: 100vh; background: var(--gray-50); }
body.index-body { background: var(--white); }
"""

final_css = global_css + "\n" + css

# Deduplicate nav blocks if necessary, but just removing body flex solves 99% of layout breaks
# Let's clean up any a { ... } duplicated rules
final_css = re.sub(r'a\s*\{\s*text-decoration:\s*none;\s*color:\s*inherit;\s*\}', '', final_css)
final_css = final_css.replace("body { font-family: 'Inter', sans-serif; color: var(--gray-900); background: var(--white); }", '')

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(final_css)

# Update admin.html to use admin-body class
with open('admin.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()
admin_html = admin_html.replace('<body>', '<body class="admin-body">')
with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_html)

# Update index.html to use index-body class
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()
index_html = index_html.replace('<body>', '<body class="index-body">')
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
