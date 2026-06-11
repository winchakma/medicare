import os
import re

# We will read index.html to extract NAV and FOOTER
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

nav_match = re.search(r'<!-- NAV -->(.*?)<!-- HERO -->', index_content, re.DOTALL)
if nav_match:
    nav_html = '<!-- NAV -->' + nav_match.group(1)
else:
    nav_html = '<nav><div class="logo"><a href="index.html">Medi<span>Care</span></a></div></nav>'

footer_match = re.search(r'<!-- FOOTER -->(.*?)</body>', index_content, re.DOTALL)
if footer_match:
    footer_html = '<!-- FOOTER -->' + footer_match.group(1)
else:
    footer_html = '<footer><p>© 2026 MediCare.</p></footer>'

def create_page(filename, title, content):
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MediCare — {title}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
{nav_html}
<div style="min-height: 70vh;">
{content}
</div>
{footer_html}
<script src="js/script.js"></script>
</body>
</html>'''
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

# 1. Update existing pages with images
def replace_images(filename):
    if not os.path.exists(filename): return
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Hero placeholder replacement
    hero_img = '<img src="image/pexels-gustavo-fring-7446987.jpg" alt="Hero" style="width:100%; max-width:460px; border-radius:16px 16px 0 0; object-fit:cover;">'
    content = re.sub(r'<div class="hero-image-placeholder">.*?</div>', hero_img, content, flags=re.DOTALL)
    
    # Doctor avatars replacements
    avatars = [
        ('SA', 'pexels-mikhail-nilov-8942498.jpg'),
        ('RK', 'pexels-pavel-danilyuk-7108238.jpg'),
        ('NI', 'pexels-rdne-6129676.jpg'),
        ('MH', 'pexels-tima-miroshnichenko-6235010.jpg')
    ]
    for initials, img_file in avatars:
        img_tag = f'<img src="image/{img_file}" style="width:100%; height:100%; border-radius:50%; object-fit:cover;">'
        content = re.sub(f'<div class="doctor-avatar"[^>]*>{initials}</div>', img_tag, content)
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

for p in ['index.html', 'doctors.html', 'doctor-profile.html', 'booking.html', 'admin.html']:
    replace_images(p)

# 2. Build new pages
create_page('confirmation.html', 'Booking Confirmed', '''
<div style="text-align:center; padding: 100px 20px;">
    <img src="image/pexels-ai25studioai-5214965.jpg" style="width:200px; border-radius:20px; margin-bottom:20px;">
    <h1 style="font-family:\'Playfair Display\',serif; color:var(--navy); font-size:36px;">Booking Confirmed!</h1>
    <p style="color:var(--gray-500); margin: 20px 0;">Your appointment has been successfully scheduled. We have sent a confirmation email.</p>
    <button class="btn-primary" onclick="location.href=\'patient-dashboard.html\'">Go to Dashboard</button>
</div>
''')

create_page('patient-dashboard.html', 'Patient Dashboard', '''
<div style="padding: 60px 5%;">
    <h2 style="font-family:\'Playfair Display\',serif; color:var(--navy); margin-bottom: 30px;">My Dashboard</h2>
    <div style="display:grid; grid-template-columns: 1fr 2fr; gap: 40px;">
        <div style="background:var(--gray-50); padding:30px; border-radius:16px;">
            <img src="image/pexels-pixabay-263337.jpg" style="width:100px; height:100px; border-radius:50%; margin-bottom:20px; object-fit:cover;">
            <h3>John Doe</h3>
            <p style="color:var(--gray-500);">Patient ID: #88921</p>
        </div>
        <div>
            <h3 style="margin-bottom:20px;">Upcoming Appointments</h3>
            <div style="border:1px solid var(--gray-200); border-radius:12px; padding:20px; display:flex; align-items:center; gap:20px;">
                <img src="image/pexels-mikhail-nilov-8942498.jpg" style="width:60px; height:60px; border-radius:50%; object-fit:cover;">
                <div>
                    <h4>Dr. Sarah Ahmed</h4>
                    <p style="color:var(--gray-500); font-size:14px;">Cardiologist • Oct 15, 10:00 AM</p>
                </div>
            </div>
        </div>
    </div>
</div>
''')

create_page('login.html', 'Login', '''
<div style="display:grid; grid-template-columns: 1fr 1fr; min-height: 80vh;">
    <div style="padding: 60px 10%; display:flex; flex-direction:column; justify-content:center;">
        <h2 style="font-family:\'Playfair Display\',serif; color:var(--navy); font-size:32px; margin-bottom: 30px;">Welcome Back</h2>
        <input type="email" placeholder="Email Address" style="width:100%; padding:14px; border:1px solid var(--gray-200); border-radius:8px; margin-bottom:16px;">
        <input type="password" placeholder="Password" style="width:100%; padding:14px; border:1px solid var(--gray-200); border-radius:8px; margin-bottom:24px;">
        <button class="btn-primary" style="width:100%; padding:14px;" onclick="location.href=\'patient-dashboard.html\'">Sign In</button>
        <p style="margin-top:20px; text-align:center; font-size:14px;">Don\'t have an account? <a href="register.html" style="color:var(--teal);">Register here</a></p>
    </div>
    <div style="background: url(\'image/pexels-rdne-6129195.jpg\') center/cover; border-radius: 40px 0 0 40px;"></div>
</div>
''')

create_page('register.html', 'Register', '''
<div style="display:grid; grid-template-columns: 1fr 1fr; min-height: 80vh;">
    <div style="background: url(\'image/pexels-rdne-6129679.jpg\') center/cover; border-radius: 0 40px 40px 0;"></div>
    <div style="padding: 60px 10%; display:flex; flex-direction:column; justify-content:center;">
        <h2 style="font-family:\'Playfair Display\',serif; color:var(--navy); font-size:32px; margin-bottom: 30px;">Create an Account</h2>
        <input type="text" placeholder="Full Name" style="width:100%; padding:14px; border:1px solid var(--gray-200); border-radius:8px; margin-bottom:16px;">
        <input type="email" placeholder="Email Address" style="width:100%; padding:14px; border:1px solid var(--gray-200); border-radius:8px; margin-bottom:16px;">
        <input type="password" placeholder="Password" style="width:100%; padding:14px; border:1px solid var(--gray-200); border-radius:8px; margin-bottom:24px;">
        <button class="btn-primary" style="width:100%; padding:14px;" onclick="location.href=\'patient-dashboard.html\'">Register</button>
        <p style="margin-top:20px; text-align:center; font-size:14px;">Are you a doctor? <a href="doctor-register.html" style="color:var(--teal);">Apply here</a></p>
    </div>
</div>
''')

create_page('doctor-register.html', 'Doctor Registration', '''
<div style="max-width:600px; margin: 60px auto; padding:40px; background:white; border:1px solid var(--gray-200); border-radius:16px; box-shadow:0 8px 30px rgba(0,0,0,0.05);">
    <h2 style="font-family:\'Playfair Display\',serif; color:var(--navy); font-size:32px; margin-bottom: 30px; text-align:center;">Join as a Doctor</h2>
    <input type="text" placeholder="Full Name" style="width:100%; padding:14px; border:1px solid var(--gray-200); border-radius:8px; margin-bottom:16px;">
    <input type="text" placeholder="Medical License Number" style="width:100%; padding:14px; border:1px solid var(--gray-200); border-radius:8px; margin-bottom:16px;">
    <input type="text" placeholder="Specialty" style="width:100%; padding:14px; border:1px solid var(--gray-200); border-radius:8px; margin-bottom:24px;">
    <button class="btn-primary" style="width:100%; padding:14px;" onclick="location.href=\'admin.html\'">Submit Application</button>
</div>
''')

create_page('specialties.html', 'Specialties', '''
<section class="section">
  <div class="section-header" style="text-align:center; display:block;">
    <div class="section-eyebrow">Comprehensive Care</div>
    <div class="section-title">All Medical Specialties</div>
  </div>
  <div class="specialties-grid" style="margin-top:40px;">
    <div class="specialty-card"><img src="image/pexels-nuptune-7966285.jpg" style="width:100%; height:120px; object-fit:cover; border-radius:8px; margin-bottom:10px;"><div class="specialty-name">Cardiology</div></div>
    <div class="specialty-card"><img src="image/pexels-rdne-6129676.jpg" style="width:100%; height:120px; object-fit:cover; border-radius:8px; margin-bottom:10px;"><div class="specialty-name">Neurology</div></div>
    <div class="specialty-card"><img src="image/pexels-mikhail-nilov-8942636.jpg" style="width:100%; height:120px; object-fit:cover; border-radius:8px; margin-bottom:10px;"><div class="specialty-name">Dentistry</div></div>
    <div class="specialty-card"><img src="image/pexels-pavel-danilyuk-7108238.jpg" style="width:100%; height:120px; object-fit:cover; border-radius:8px; margin-bottom:10px;"><div class="specialty-name">Pediatrics</div></div>
  </div>
</section>
''')

create_page('blog.html', 'Health Blog', '''
<section class="section">
  <h2 style="font-family:\'Playfair Display\',serif; color:var(--navy); font-size:36px; margin-bottom: 40px; text-align:center;">Latest Health Tips</h2>
  <div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap:30px;">
    <div style="border:1px solid var(--gray-200); border-radius:12px; overflow:hidden;">
      <img src="image/pexels-mikhail-nilov-8942636.jpg" style="width:100%; height:200px; object-fit:cover;">
      <div style="padding:20px;">
        <h3 style="margin-bottom:10px; font-size:18px;">How to manage daily stress</h3>
        <p style="color:var(--gray-500); font-size:14px; margin-bottom:20px;">Stress is a silent killer. Learn 5 techniques to manage your daily anxiety levels effectively.</p>
        <a href="#" style="color:var(--teal); font-weight:600; font-size:14px;">Read More →</a>
      </div>
    </div>
    <div style="border:1px solid var(--gray-200); border-radius:12px; overflow:hidden;">
      <img src="image/pexels-nuptune-7966285.jpg" style="width:100%; height:200px; object-fit:cover;">
      <div style="padding:20px;">
        <h3 style="margin-bottom:10px; font-size:18px;">Benefits of regular checkups</h3>
        <p style="color:var(--gray-500); font-size:14px; margin-bottom:20px;">Preventative care is the best care. Why you shouldn\'t skip your annual physical.</p>
        <a href="#" style="color:var(--teal); font-weight:600; font-size:14px;">Read More →</a>
      </div>
    </div>
  </div>
</section>
''')

create_page('about.html', 'About Us', '''
<div style="padding: 60px 5%; display:grid; grid-template-columns: 1fr 1fr; gap:60px; align-items:center;">
    <div>
        <h2 style="font-family:\'Playfair Display\',serif; color:var(--navy); font-size:36px; margin-bottom: 20px;">Transforming Healthcare Access</h2>
        <p style="color:var(--gray-500); line-height:1.7; margin-bottom:20px;">MediCare was founded with a simple mission: to make finding and booking the right doctor as simple as booking a hotel. No more waiting on hold, no more guesswork.</p>
        <p style="color:var(--gray-500); line-height:1.7;">We partner with thousands of verified specialists to bring world-class healthcare directly to your fingertips.</p>
    </div>
    <div>
        <img src="image/pexels-tima-miroshnichenko-6235010.jpg" style="width:100%; border-radius:24px; box-shadow:0 20px 40px rgba(0,0,0,0.1);">
    </div>
</div>
''')

create_page('contact.html', 'Contact Us', '''
<div style="max-width:600px; margin: 60px auto; padding:40px; background:white; border:1px solid var(--gray-200); border-radius:16px; text-align:center;">
    <h2 style="font-family:\'Playfair Display\',serif; color:var(--navy); font-size:32px; margin-bottom: 10px;">Get in Touch</h2>
    <p style="color:var(--gray-500); margin-bottom:30px;">Our support team is available 24/7 to assist you.</p>
    <input type="text" placeholder="Name" style="width:100%; padding:14px; border:1px solid var(--gray-200); border-radius:8px; margin-bottom:16px;">
    <input type="email" placeholder="Email" style="width:100%; padding:14px; border:1px solid var(--gray-200); border-radius:8px; margin-bottom:16px;">
    <textarea placeholder="Your Message" rows="5" style="width:100%; padding:14px; border:1px solid var(--gray-200); border-radius:8px; margin-bottom:24px; font-family:inherit;"></textarea>
    <button class="btn-primary" style="width:100%; padding:14px;">Send Message</button>
</div>
''')

create_page('privacy.html', 'Privacy Policy', '''
<div style="max-width:800px; margin: 60px auto; padding: 0 20px;">
    <h1 style="font-family:\'Playfair Display\',serif; color:var(--navy); font-size:36px; margin-bottom: 30px;">Privacy Policy</h1>
    <div style="color:var(--gray-700); line-height:1.8;">
        <p style="margin-bottom:20px;">Last updated: October 2026</p>
        <h3 style="margin-bottom:10px; color:var(--navy);">1. Information We Collect</h3>
        <p style="margin-bottom:20px;">We collect personal health information necessary for your bookings, including names, contact details, and medical history shared with your doctors.</p>
        <h3 style="margin-bottom:10px; color:var(--navy);">2. How We Use Information</h3>
        <p style="margin-bottom:20px;">Your information is strictly used to facilitate healthcare services and is never sold to third parties.</p>
        <h3 style="margin-bottom:10px; color:var(--navy);">3. Data Security</h3>
        <p style="margin-bottom:20px;">We employ state-of-the-art encryption to protect your sensitive medical data.</p>
    </div>
</div>
''')

create_page('terms.html', 'Terms of Service', '''
<div style="max-width:800px; margin: 60px auto; padding: 0 20px;">
    <h1 style="font-family:\'Playfair Display\',serif; color:var(--navy); font-size:36px; margin-bottom: 30px;">Terms of Service</h1>
    <div style="color:var(--gray-700); line-height:1.8;">
        <p style="margin-bottom:20px;">Last updated: October 2026</p>
        <h3 style="margin-bottom:10px; color:var(--navy);">1. Acceptance of Terms</h3>
        <p style="margin-bottom:20px;">By using MediCare, you agree to these terms. If you disagree, do not use the service.</p>
        <h3 style="margin-bottom:10px; color:var(--navy);">2. Medical Disclaimer</h3>
        <p style="margin-bottom:20px;">MediCare is a platform to connect you with doctors. It is not a replacement for emergency medical services. In an emergency, dial your local emergency number.</p>
        <h3 style="margin-bottom:10px; color:var(--navy);">3. Payment & Cancellations</h3>
        <p style="margin-bottom:20px;">Bookings can be cancelled up to 24 hours in advance for a full refund.</p>
    </div>
</div>
''')

create_page('symptom-checker.html', 'AI Symptom Checker', '''
<div style="max-width:800px; margin: 60px auto; padding:40px; background:white; border:1px solid var(--gray-200); border-radius:16px; text-align:center;">
    <div style="width:80px; height:80px; border-radius:50%; background:var(--teal-light); display:flex; align-items:center; justify-content:center; font-size:32px; margin:0 auto 20px;">🤖</div>
    <h2 style="font-family:\'Playfair Display\',serif; color:var(--navy); font-size:32px; margin-bottom: 10px;">AI Symptom Checker</h2>
    <p style="color:var(--gray-500); margin-bottom:30px;">Describe what you\'re feeling, and our AI will recommend the right specialist for you.</p>
    <textarea placeholder="E.g., I have had a severe headache for 3 days and I feel dizzy when I stand up..." rows="4" style="width:100%; padding:14px; border:1px solid var(--gray-200); border-radius:8px; margin-bottom:24px; font-family:inherit;"></textarea>
    <button class="btn-primary" style="padding:14px 30px;">Analyze Symptoms</button>
</div>
''')

create_page('chat-support.html', 'AI Chat Support', '''
<div style="max-width:600px; margin: 40px auto; border:1px solid var(--gray-200); border-radius:16px; overflow:hidden;">
    <div style="background:var(--navy); padding:20px; color:white; display:flex; align-items:center; gap:12px;">
        <div style="width:40px; height:40px; border-radius:50%; background:white; display:flex; align-items:center; justify-content:center; font-size:20px;">💬</div>
        <div>
            <h3 style="font-size:16px; margin:0;">MediCare Assistant</h3>
            <span style="font-size:12px; color:#5DCAA5;">Online 24/7</span>
        </div>
    </div>
    <div style="height:400px; background:var(--gray-50); padding:20px; display:flex; flex-direction:column; gap:16px; overflow-y:auto;">
        <div style="align-self:flex-start; background:white; padding:12px 16px; border-radius:16px 16px 16px 0; border:1px solid var(--gray-200); max-width:80%;">
            Hello! I\'m the MediCare AI Assistant. How can I help you today?
        </div>
    </div>
    <div style="padding:16px; background:white; border-top:1px solid var(--gray-200); display:flex; gap:10px;">
        <input type="text" placeholder="Type your message..." style="flex:1; padding:12px; border:1px solid var(--gray-200); border-radius:24px; outline:none;">
        <button class="btn-primary" style="border-radius:24px; padding:0 24px;">Send</button>
    </div>
</div>
''')
