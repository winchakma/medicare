import os

role_html = """
        <div class="auth-field" style="margin-bottom: 15px;">
          <label>I am a...</label>
          <div style="display:flex; gap:15px; margin-top:5px;">
            <label style="display:flex; align-items:center; gap:5px; font-size:14px; color:var(--gray-700); cursor:pointer; text-transform:none;"><input type="radio" name="register-role" value="patient" checked> Patient</label>
            <label style="display:flex; align-items:center; gap:5px; font-size:14px; color:var(--gray-700); cursor:pointer; text-transform:none;"><input type="radio" name="register-role" value="doctor"> Doctor</label>
          </div>
        </div>
        
        <div class="auth-row">"""

def update_files():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    for f in html_files:
        with open(f, 'r', encoding='utf-8') as file:
            html = file.read()
        
        # We need to insert it right before `<div class="auth-row">` inside `#register-form`
        if '<div class="auth-row">' in html and 'I am a...' not in html:
            # We want to replace the FIRST occurrence of `<div class="auth-row">` after `<form id="register-form"`
            parts = html.split('<form id="register-form"')
            if len(parts) > 1:
                sub_parts = parts[1].split('<div class="auth-row">', 1)
                if len(sub_parts) > 1:
                    new_html = parts[0] + '<form id="register-form"' + sub_parts[0] + role_html + sub_parts[1]
                    with open(f, 'w', encoding='utf-8') as file:
                        file.write(new_html)

if __name__ == '__main__':
    update_files()
    print("UI updated.")
