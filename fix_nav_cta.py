import os
import glob
import re

for filepath in glob.glob(r"c:\Users\user\Desktop\doctor\frontend\*.html"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Case 1: The button exists inside </nav> but is NOT wrapped in .nav-cta
    # We look for <button class="btn-primary" onclick="openAuthModal('login')">Sign In</button>
    # And check if it's preceded by <div class="nav-cta">
    
    # Let's just find the button:
    button_html = """<button class="btn-primary" onclick="openAuthModal('login')">Sign In</button>"""
    wrapped_html = """<div class="nav-cta">
    <button class="btn-primary" onclick="openAuthModal('login')">Sign In</button>
  </div>"""

    if button_html in content and '<div class="nav-cta">' not in content:
        # It's not wrapped in nav-cta at all
        content = content.replace(button_html, wrapped_html)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed {filepath}")
    elif '<div class="nav-cta">' in content and button_html in content:
        # Check if the button is actually inside nav-cta. Usually it is.
        # But if there's an unwrapped one, we might need to be careful.
        # It's better to just check if there's a stray button.
        pass

print("Done checking all files.")
