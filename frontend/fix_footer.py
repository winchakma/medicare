import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

# 1. Update style.css
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Make index-body a flex column so footer sticks to bottom
if 'body.index-body { background: var(--white); }' in css:
    css = css.replace('body.index-body { background: var(--white); }', 
                      'body.index-body { background: var(--white); display: flex; flex-direction: column; min-height: 100vh; }\n.main-content { flex: 1; }')
else:
    # Just append it if not found exactly
    css += '\nbody.index-body { display: flex; flex-direction: column; min-height: 100vh; }\n.main-content { flex: 1; }\n'

# Add rich footer styles
rich_footer_css = """
/* RICH FOOTER */
.rich-footer { background: var(--navy); color: rgba(255,255,255,0.7); padding: 60px max(5%, calc((100vw - 1200px) / 2)) 0; border-top: 1px solid rgba(255,255,255,0.06); font-family: 'Inter', sans-serif; margin-top: auto; }
.footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1.5fr; gap: 40px; margin-bottom: 40px; }
.footer-col .logo { font-size: 24px; color: white; margin-bottom: 16px; }
.footer-col p { font-size: 13px; line-height: 1.7; margin-bottom: 12px; }
.footer-col h4 { color: white; font-size: 15px; font-weight: 600; margin-bottom: 20px; }
.footer-col a { display: block; color: rgba(255,255,255,0.7); text-decoration: none; font-size: 13px; margin-bottom: 12px; transition: color .2s; }
.footer-col a:hover { color: var(--teal); }
.social-links { display: flex; gap: 12px; margin-top: 16px; }
.social-links a { width: 36px; height: 36px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; color: white; transition: background .2s; }
.social-links a:hover { background: var(--teal); }
.footer-bottom { border-top: 1px solid rgba(255,255,255,0.06); padding: 24px 0; text-align: center; font-size: 13px; color: rgba(255,255,255,0.5); }
@media (max-width: 768px) { .footer-grid { grid-template-columns: 1fr; gap: 30px; } }
"""
if 'RICH FOOTER' not in css:
    css += rich_footer_css

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# New rich footer HTML
new_footer = """<footer class="rich-footer">
  <div class="footer-grid">
    <div class="footer-col">
      <div class="logo">Medi<span style="color:#5DCAA5">Care</span></div>
      <p>Your trusted platform for finding the right doctors and booking appointments seamlessly. Real doctors, real care.</p>
    </div>
    <div class="footer-col">
      <h4>Quick Links</h4>
      <a href="doctors.html">Find Doctors</a>
      <a href="specialties.html">Specialties</a>
      <a href="blog.html">Health Blog</a>
      <a href="about.html">About Us</a>
    </div>
    <div class="footer-col">
      <h4>Support</h4>
      <a href="contact.html">Contact Us</a>
      <a href="terms.html">Terms of Service</a>
      <a href="privacy.html">Privacy Policy</a>
      <a href="#">FAQ</a>
    </div>
    <div class="footer-col">
      <h4>Contact</h4>
      <p>Email: support@medicare.com</p>
      <p>Phone: +1 (555) 123-4567</p>
      <div class="social-links">
        <a href="#" style="font-weight:bold">FB</a>
        <a href="#" style="font-weight:bold">TW</a>
        <a href="#" style="font-weight:bold">IG</a>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2026 MediCare. All rights reserved.</p>
  </div>
</footer>"""

for f in html_files:
    if f == 'admin.html' or f == 'patient-dashboard.html':
        continue # Dashboards usually don't have this big footer
        
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Add main-content wrapper if it's index-body
    if '<body class="index-body">' in content:
        # Check if already wrapped
        if '<div class="main-content">' not in content:
            # We want to wrap everything between nav and footer in main-content
            # Actually, simpler: just let flex: 1 apply to whatever section is main.
            pass
            
    # Remove old footer completely
    content = re.sub(r'<footer.*?</footer>', '', content, flags=re.DOTALL)
    
    # If the file has a script tag at the end, insert footer before script tag
    if '<script' in content:
        content = content.replace('<script', new_footer + '\n<script', 1)
    else:
        # insert before </body>
        content = content.replace('</body>', new_footer + '\n</body>')
        
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

# 3. Create missing pages: contact.html, terms.html, privacy.html
template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — MediCare</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body class="index-body">
<nav>
  <div class="logo"><a href="index.html" style="color:inherit; text-decoration:none;">Medi<span>Care</span></a></div>
  <div class="nav-links">
    <a href="doctors.html">Find Doctors</a>
    <a href="specialties.html">Specialties</a>
    <a href="blog.html">Health Blog</a>
    <a href="about.html">About Us</a>
  </div>
  <div class="nav-cta">
    <button class="btn-outline" onclick="location.href='login.html'">Sign In</button>
    <button class="btn-primary" onclick="location.href='login.html'">Register</button>
  </div>
</nav>

<section class="section" style="flex:1;">
  <div class="section-header" style="text-align:center; display:block; margin-bottom: 40px;">
    <div class="section-title">{title}</div>
  </div>
  <div style="max-width:800px; margin:0 auto; font-size:15px; color:var(--gray-700); line-height:1.7;">
    {content}
  </div>
</section>

{footer}
</body>
</html>"""

contact_content = """
<p style="text-align:center; margin-bottom: 30px;">Have questions? We'd love to hear from you. Send us a message and we'll respond as soon as possible.</p>
<form style="display:flex; flex-direction:column; gap:20px; background:white; padding:30px; border-radius:16px; border:1px solid var(--gray-200);">
  <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">
    <div><label style="font-size:13px; font-weight:600; margin-bottom:8px; display:block;">First Name</label><input type="text" style="width:100%; padding:12px; border:1px solid var(--gray-200); border-radius:8px;"></div>
    <div><label style="font-size:13px; font-weight:600; margin-bottom:8px; display:block;">Last Name</label><input type="text" style="width:100%; padding:12px; border:1px solid var(--gray-200); border-radius:8px;"></div>
  </div>
  <div><label style="font-size:13px; font-weight:600; margin-bottom:8px; display:block;">Email Address</label><input type="email" style="width:100%; padding:12px; border:1px solid var(--gray-200); border-radius:8px;"></div>
  <div><label style="font-size:13px; font-weight:600; margin-bottom:8px; display:block;">Message</label><textarea style="width:100%; padding:12px; border:1px solid var(--gray-200); border-radius:8px; min-height:120px;"></textarea></div>
  <button type="button" style="padding:14px; background:var(--teal); color:white; border:none; border-radius:8px; font-size:15px; font-weight:600; cursor:pointer;">Send Message</button>
</form>
"""

terms_content = """
<h3 style="color:var(--navy); margin-bottom:10px;">1. Acceptance of Terms</h3>
<p style="margin-bottom:20px;">By accessing and using MediCare, you accept and agree to be bound by the terms and provision of this agreement.</p>
<h3 style="color:var(--navy); margin-bottom:10px;">2. Medical Disclaimer</h3>
<p style="margin-bottom:20px;">The content provided on MediCare is for informational purposes only and is not intended as a substitute for professional medical advice, diagnosis, or treatment.</p>
<h3 style="color:var(--navy); margin-bottom:10px;">3. User Responsibilities</h3>
<p style="margin-bottom:20px;">Users must provide accurate information when booking appointments. Cancellations must be made at least 24 hours in advance.</p>
"""

privacy_content = """
<h3 style="color:var(--navy); margin-bottom:10px;">1. Information Collection</h3>
<p style="margin-bottom:20px;">We collect information you provide directly to us, such as when you create or modify your account, request services, contact customer support, or otherwise communicate with us.</p>
<h3 style="color:var(--navy); margin-bottom:10px;">2. Use of Information</h3>
<p style="margin-bottom:20px;">We may use the information we collect about you to provide, maintain, and improve our services, including to facilitate medical bookings and communications between you and healthcare providers.</p>
<h3 style="color:var(--navy); margin-bottom:10px;">3. Data Security</h3>
<p style="margin-bottom:20px;">We implement reasonable security measures designed to protect your personal and medical information from unauthorized access, disclosure, or destruction. We comply with HIPAA data standards where applicable.</p>
"""

with open('contact.html', 'w', encoding='utf-8') as f: f.write(template.replace('{title}', 'Contact Us').replace('{content}', contact_content).replace('{footer}', new_footer))
with open('terms.html', 'w', encoding='utf-8') as f: f.write(template.replace('{title}', 'Terms of Service').replace('{content}', terms_content).replace('{footer}', new_footer))
with open('privacy.html', 'w', encoding='utf-8') as f: f.write(template.replace('{title}', 'Privacy Policy').replace('{content}', privacy_content).replace('{footer}', new_footer))

print("Rich footer applied and contact/terms/privacy pages created.")
