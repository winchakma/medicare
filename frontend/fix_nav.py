import os
import glob

html_files = glob.glob('c:/Users/user/Desktop/doctor/frontend/*.html')

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<div class="nav-links">' in content and '<a href="index.html">Home</a>' not in content:
        content = content.replace(
            '<div class="nav-links">\n    <a href="doctors.html">Find Doctors</a>',
            '<div class="nav-links">\n    <a href="index.html">Home</a>\n    <a href="doctors.html">Find Doctors</a>'
        )
        # Also handle potential single quote or different spacing
        content = content.replace(
            '<div class="nav-links">\n      <a href="doctors.html">Find Doctors</a>',
            '<div class="nav-links">\n      <a href="index.html">Home</a>\n      <a href="doctors.html">Find Doctors</a>'
        )
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")
