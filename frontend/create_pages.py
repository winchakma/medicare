import os
import re

# 1. Update navigation links in all HTML files
html_files = [f for f in os.listdir('.') if f.endswith('.html')]
for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace the exact nav links
    content = content.replace('<a href="#">Specialties</a>', '<a href="specialties.html">Specialties</a>')
    content = content.replace('<a href="#">Health Blog</a>', '<a href="blog.html">Health Blog</a>')
    content = content.replace('<a href="#">About Us</a>', '<a href="about.html">About Us</a>')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

# 2. Create specialties.html
specialties_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Specialties — MediCare</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body class="index-body">
<nav>
  <div class="logo"><a href="index.html" style="color:inherit; text-decoration:none;">Medi<span>Care</span></a></div>
  <div class="nav-links">
    <a href="doctors.html">Find Doctors</a>
    <a href="specialties.html" style="color:var(--teal)">Specialties</a>
    <a href="blog.html">Health Blog</a>
    <a href="about.html">About Us</a>
  </div>
  <div class="nav-cta">
    <button class="btn-outline" onclick="location.href='login.html'">Sign In</button>
    <button class="btn-primary" onclick="location.href='login.html'">Register</button>
  </div>
</nav>

<section class="section">
  <div class="section-header" style="text-align:center; display:block;">
    <div class="section-eyebrow">Comprehensive Care</div>
    <div class="section-title">Medical Specialties</div>
    <p style="color:var(--gray-500); margin-top:10px;">Find top-rated doctors across all major medical fields.</p>
  </div>
  <div class="specialties-grid" style="grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
    <!-- Large specialty cards -->
    <div class="specialty-card" onclick="location.href='doctors.html'" style="padding: 30px;"><div class="specialty-icon" style="background:#FFE4E1; width:60px; height:60px; font-size:28px;">❤️</div><div class="specialty-name" style="font-size:16px;">Cardiology</div><div class="specialty-count">48 doctors</div></div>
    <div class="specialty-card" onclick="location.href='doctors.html'" style="padding: 30px;"><div class="specialty-icon" style="background:#E1F5EE; width:60px; height:60px; font-size:28px;">🧠</div><div class="specialty-name" style="font-size:16px;">Neurology</div><div class="specialty-count">32 doctors</div></div>
    <div class="specialty-card" onclick="location.href='doctors.html'" style="padding: 30px;"><div class="specialty-icon" style="background:#FFF3E0; width:60px; height:60px; font-size:28px;">🦷</div><div class="specialty-name" style="font-size:16px;">Dentistry</div><div class="specialty-count">67 doctors</div></div>
    <div class="specialty-card" onclick="location.href='doctors.html'" style="padding: 30px;"><div class="specialty-icon" style="background:#E3F2FD; width:60px; height:60px; font-size:28px;">👶</div><div class="specialty-name" style="font-size:16px;">Pediatrics</div><div class="specialty-count">41 doctors</div></div>
    <div class="specialty-card" onclick="location.href='doctors.html'" style="padding: 30px;"><div class="specialty-icon" style="background:#F3E5F5; width:60px; height:60px; font-size:28px;">🦴</div><div class="specialty-name" style="font-size:16px;">Orthopedic</div><div class="specialty-count">29 doctors</div></div>
    <div class="specialty-card" onclick="location.href='doctors.html'" style="padding: 30px;"><div class="specialty-icon" style="background:#E8F5E9; width:60px; height:60px; font-size:28px;">👁️</div><div class="specialty-name" style="font-size:16px;">Ophthalmology</div><div class="specialty-count">22 doctors</div></div>
    <div class="specialty-card" onclick="location.href='doctors.html'" style="padding: 30px;"><div class="specialty-icon" style="background:#FFF8E1; width:60px; height:60px; font-size:28px;">🩺</div><div class="specialty-name" style="font-size:16px;">General</div><div class="specialty-count">95 doctors</div></div>
    <div class="specialty-card" onclick="location.href='doctors.html'" style="padding: 30px;"><div class="specialty-icon" style="background:#FCE4EC; width:60px; height:60px; font-size:28px;">🧬</div><div class="specialty-name" style="font-size:16px;">Dermatology</div><div class="specialty-count">38 doctors</div></div>
  </div>
</section>
<footer><p>© 2026 MediCare. All rights reserved.</p></footer>
</body>
</html>"""
with open('specialties.html', 'w', encoding='utf-8') as f:
    f.write(specialties_html)

# 3. Create blog.html
blog_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Health Blog — MediCare</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body class="index-body">
<nav>
  <div class="logo"><a href="index.html" style="color:inherit; text-decoration:none;">Medi<span>Care</span></a></div>
  <div class="nav-links">
    <a href="doctors.html">Find Doctors</a>
    <a href="specialties.html">Specialties</a>
    <a href="blog.html" style="color:var(--teal)">Health Blog</a>
    <a href="about.html">About Us</a>
  </div>
  <div class="nav-cta">
    <button class="btn-outline" onclick="location.href='login.html'">Sign In</button>
    <button class="btn-primary" onclick="location.href='login.html'">Register</button>
  </div>
</nav>

<section class="section">
  <div class="section-header" style="text-align:center; display:block; margin-bottom: 40px;">
    <div class="section-eyebrow">Insights & Tips</div>
    <div class="section-title">Health & Wellness Blog</div>
    <p style="color:var(--gray-500); margin-top:10px;">Expert advice and health articles written by our medical professionals.</p>
  </div>
  
  <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:24px;">
    <div style="border: 1px solid var(--gray-200); border-radius: 16px; overflow:hidden;">
      <div style="height:200px; background:var(--teal-light);"></div>
      <div style="padding:20px;">
        <div style="font-size:12px; color:var(--teal); font-weight:600; margin-bottom:8px;">CARDIOLOGY</div>
        <h3 style="font-family:'Playfair Display',serif; font-size:20px; color:var(--navy); margin-bottom:10px;">10 Tips for a Healthy Heart</h3>
        <p style="font-size:14px; color:var(--gray-500); line-height:1.6;">Simple daily habits that can significantly reduce your risk of cardiovascular disease...</p>
      </div>
    </div>
    <div style="border: 1px solid var(--gray-200); border-radius: 16px; overflow:hidden;">
      <div style="height:200px; background:#FFE4E1;"></div>
      <div style="padding:20px;">
        <div style="font-size:12px; color:var(--teal); font-weight:600; margin-bottom:8px;">NUTRITION</div>
        <h3 style="font-family:'Playfair Display',serif; font-size:20px; color:var(--navy); margin-bottom:10px;">The Truth About Vitamins</h3>
        <p style="font-size:14px; color:var(--gray-500); line-height:1.6;">Do you really need supplements? Our leading dietitians break down the science...</p>
      </div>
    </div>
    <div style="border: 1px solid var(--gray-200); border-radius: 16px; overflow:hidden;">
      <div style="height:200px; background:#E3F2FD;"></div>
      <div style="padding:20px;">
        <div style="font-size:12px; color:var(--teal); font-weight:600; margin-bottom:8px;">MENTAL HEALTH</div>
        <h3 style="font-family:'Playfair Display',serif; font-size:20px; color:var(--navy); margin-bottom:10px;">Managing Stress at Work</h3>
        <p style="font-size:14px; color:var(--gray-500); line-height:1.6;">Practical mental health strategies to prevent burnout in high-pressure environments...</p>
      </div>
    </div>
  </div>
</section>
<footer><p>© 2026 MediCare. All rights reserved.</p></footer>
</body>
</html>"""
with open('blog.html', 'w', encoding='utf-8') as f:
    f.write(blog_html)

# 4. Create about.html
about_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>About Us — MediCare</title>
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
    <a href="about.html" style="color:var(--teal)">About Us</a>
  </div>
  <div class="nav-cta">
    <button class="btn-outline" onclick="location.href='login.html'">Sign In</button>
    <button class="btn-primary" onclick="location.href='login.html'">Register</button>
  </div>
</nav>

<section class="section" style="text-align:center;">
  <h1 style="font-family:'Playfair Display',serif; font-size:40px; color:var(--navy); margin-bottom:20px;">Revolutionizing Healthcare Access</h1>
  <p style="max-width:700px; margin:0 auto; font-size:16px; color:var(--gray-700); line-height:1.7;">
    At MediCare, we believe that accessing top-tier medical professionals should be simple, transparent, and immediate. We connect thousands of patients with verified doctors across the country for both in-person and secure video consultations. Our mission is to make healthcare seamless, giving you the power to control your health schedule without the wait.
  </p>
  
  <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:24px; max-width:800px; margin:60px auto 0;">
    <div style="padding:30px; border:1px solid var(--gray-200); border-radius:16px;">
      <h3 style="color:var(--navy); font-size:24px; margin-bottom:8px;">500+</h3>
      <p style="color:var(--gray-500); font-size:14px;">Verified Specialists</p>
    </div>
    <div style="padding:30px; border:1px solid var(--gray-200); border-radius:16px;">
      <h3 style="color:var(--navy); font-size:24px; margin-bottom:8px;">24/7</h3>
      <p style="color:var(--gray-500); font-size:14px;">AI Support & Booking</p>
    </div>
    <div style="padding:30px; border:1px solid var(--gray-200); border-radius:16px;">
      <h3 style="color:var(--navy); font-size:24px; margin-bottom:8px;">99%</h3>
      <p style="color:var(--gray-500); font-size:14px;">Patient Satisfaction</p>
    </div>
  </div>
</section>
<footer><p>© 2026 MediCare. All rights reserved.</p></footer>
</body>
</html>"""
with open('about.html', 'w', encoding='utf-8') as f:
    f.write(about_html)

print("Created supporting pages and updated navigation links.")
