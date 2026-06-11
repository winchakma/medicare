import os
import re

modal_html = """
<!-- AUTH MODAL -->
<div id="auth-modal" class="auth-modal-overlay">
  <div class="auth-modal-container">
    <button class="auth-modal-close" onclick="closeAuthModal()"><i class="fas fa-times"></i></button>
    <div class="auth-modal-left">
      <div class="auth-modal-logo">Medi<span>Care</span></div>
      <h2>Welcome Back</h2>
      <p>Sign in or create an account to book appointments, manage your health records, and connect with top specialists.</p>
    </div>
    <div class="auth-modal-right">
      <div class="auth-tabs">
        <button class="auth-tab active" onclick="switchAuthTab('login')">Sign In</button>
        <button class="auth-tab" onclick="switchAuthTab('register')">Register</button>
      </div>
      
      <!-- Login Form -->
      <form id="login-form" class="auth-form active" onsubmit="handleLogin(event)">
        <div class="auth-field">
          <label>Email Address</label>
          <input type="email" id="login-email" required placeholder="name@example.com">
        </div>
        <div class="auth-field">
          <label>Password</label>
          <input type="password" id="login-password" required placeholder="••••••••">
        </div>
        <button type="submit" class="auth-submit-btn">Sign In <i class="fas fa-arrow-right"></i></button>
        <div id="login-error" class="auth-error"></div>
      </form>

      <!-- Register Form -->
      <form id="register-form" class="auth-form" onsubmit="handleRegister(event)">
        <div class="auth-row">
          <div class="auth-field">
            <label>First Name</label>
            <input type="text" id="register-fname" required placeholder="John">
          </div>
          <div class="auth-field">
            <label>Last Name</label>
            <input type="text" id="register-lname" required placeholder="Doe">
          </div>
        </div>
        <div class="auth-field">
          <label>Email Address</label>
          <input type="email" id="register-email" required placeholder="name@example.com">
        </div>
        <div class="auth-field">
          <label>Password</label>
          <input type="password" id="register-password" required placeholder="Create a password">
        </div>
        <button type="submit" class="auth-submit-btn">Create Account <i class="fas fa-user-plus"></i></button>
        <div id="register-error" class="auth-error"></div>
        <div id="register-success" class="auth-success"></div>
      </form>
    </div>
  </div>
</div>
"""

css_code = """
/* AUTH MODAL */
.auth-modal-overlay {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(10, 22, 40, 0.6); backdrop-filter: blur(8px);
  z-index: 1000; display: flex; align-items: center; justify-content: center;
  opacity: 0; pointer-events: none; transition: opacity 0.3s ease;
}
.auth-modal-overlay.active { opacity: 1; pointer-events: auto; }

.auth-modal-container {
  background: white; border-radius: 24px; overflow: hidden;
  width: 90%; max-width: 850px; display: flex;
  box-shadow: 0 24px 60px rgba(0,0,0,0.2);
  transform: translateY(30px) scale(0.95); transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative; min-height: 500px;
}
.auth-modal-overlay.active .auth-modal-container {
  transform: translateY(0) scale(1);
}

.auth-modal-close {
  position: absolute; top: 20px; right: 20px; width: 36px; height: 36px;
  background: var(--gray-50); border: 1px solid var(--gray-200); border-radius: 50%;
  font-size: 16px; color: var(--gray-500); cursor: pointer;
  display: flex; align-items: center; justify-content: center; z-index: 10;
  transition: all 0.2s;
}
.auth-modal-close:hover { background: var(--red); color: white; border-color: var(--red); transform: rotate(90deg); }

.auth-modal-left {
  flex: 1; background: linear-gradient(135deg, #0A1628, #0D4A38);
  padding: 48px; color: white; display: flex; flex-direction: column; justify-content: center;
  position: relative; overflow: hidden;
}
.auth-modal-left::before {
  content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
  background: radial-gradient(circle at center, rgba(93, 202, 165, 0.15) 0%, transparent 60%);
  animation: pulseBg 10s infinite alternate linear;
}
@keyframes pulseBg { 0% { transform: scale(1); } 100% { transform: scale(1.2); } }

.auth-modal-logo { font-family: 'Playfair Display', serif; font-size: 28px; margin-bottom: 24px; position: relative; z-index: 1; }
.auth-modal-logo span { color: #5DCAA5; }
.auth-modal-left h2 { font-family: 'Playfair Display', serif; font-size: 32px; margin-bottom: 16px; position: relative; z-index: 1; }
.auth-modal-left p { font-size: 15px; color: rgba(255,255,255,0.7); line-height: 1.6; position: relative; z-index: 1; }

.auth-modal-right { flex: 1.2; padding: 48px 40px; background: white; position: relative; }

.auth-tabs { display: flex; gap: 8px; margin-bottom: 32px; background: var(--gray-50); padding: 6px; border-radius: 12px; }
.auth-tab {
  flex: 1; padding: 12px; border: none; background: transparent; border-radius: 8px;
  font-size: 14px; font-weight: 600; color: var(--gray-500); cursor: pointer; transition: all 0.2s;
}
.auth-tab.active { background: white; color: var(--navy); box-shadow: 0 2px 10px rgba(0,0,0,0.05); }

.auth-form { display: none; animation: fadeIn 0.3s ease; }
.auth-form.active { display: block; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

.auth-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.auth-field { margin-bottom: 20px; }
.auth-field label { display: block; font-size: 12px; font-weight: 600; color: var(--gray-700); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em; }
.auth-field input {
  width: 100%; padding: 14px 16px; border: 1.5px solid var(--gray-200); border-radius: 10px;
  font-size: 15px; color: var(--gray-900); font-family: 'Inter', sans-serif; transition: all 0.2s; background: var(--gray-50);
}
.auth-field input:focus { border-color: var(--teal); background: white; box-shadow: 0 0 0 4px rgba(13,155,118,0.1); outline: none; }

.auth-submit-btn {
  width: 100%; padding: 16px; background: var(--navy); color: white; border: none; border-radius: 10px;
  font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; gap: 10px; margin-top: 10px;
}
.auth-submit-btn:hover { background: var(--teal); transform: translateY(-2px); box-shadow: 0 8px 20px rgba(13,155,118,0.2); }

.auth-error { color: var(--red); font-size: 13px; margin-top: 12px; text-align: center; font-weight: 500; min-height: 18px; }
.auth-success { color: var(--green); font-size: 13px; margin-top: 12px; text-align: center; font-weight: 500; min-height: 18px; }

@media (max-width: 768px) {
  .auth-modal-container { flex-direction: column; max-height: 90vh; overflow-y: auto; }
  .auth-modal-left { display: none; }
  .auth-modal-right { padding: 32px 24px; }
}
"""

js_code = """
// --- AUTH MODAL LOGIC ---

function openAuthModal(tab = 'login') {
  const modal = document.getElementById('auth-modal');
  if (modal) {
    modal.classList.add('active');
    switchAuthTab(tab);
  }
}

function closeAuthModal() {
  const modal = document.getElementById('auth-modal');
  if (modal) {
    modal.classList.remove('active');
    // Clear forms
    document.getElementById('login-form').reset();
    document.getElementById('register-form').reset();
    document.getElementById('login-error').innerText = '';
    document.getElementById('register-error').innerText = '';
    document.getElementById('register-success').innerText = '';
  }
}

function switchAuthTab(tab) {
  const loginTab = document.querySelectorAll('.auth-tab')[0];
  const registerTab = document.querySelectorAll('.auth-tab')[1];
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');
  
  if (tab === 'login') {
    loginTab.classList.add('active');
    registerTab.classList.remove('active');
    loginForm.classList.add('active');
    registerForm.classList.remove('active');
  } else {
    registerTab.classList.add('active');
    loginTab.classList.remove('active');
    registerForm.classList.add('active');
    loginForm.classList.remove('active');
  }
}

async function handleLogin(e) {
  e.preventDefault();
  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;
  const errorEl = document.getElementById('login-error');
  errorEl.innerText = '';
  
  try {
    const btn = document.querySelector('#login-form button');
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    btn.disabled = true;

    const res = await fetch('http://localhost:8000/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Login failed');
    }
    
    // Success
    localStorage.setItem('medicare_token', data.access_token);
    btn.innerHTML = 'Success <i class="fas fa-check"></i>';
    btn.style.background = 'var(--green)';
    
    setTimeout(() => {
      closeAuthModal();
      window.location.reload();
    }, 1000);
    
  } catch (err) {
    errorEl.innerText = err.message;
    const btn = document.querySelector('#login-form button');
    btn.innerHTML = 'Sign In <i class="fas fa-arrow-right"></i>';
    btn.disabled = false;
  }
}

async function handleRegister(e) {
  e.preventDefault();
  const firstName = document.getElementById('register-fname').value;
  const lastName = document.getElementById('register-lname').value;
  const email = document.getElementById('register-email').value;
  const password = document.getElementById('register-password').value;
  const errorEl = document.getElementById('register-error');
  const successEl = document.getElementById('register-success');
  
  errorEl.innerText = '';
  successEl.innerText = '';
  
  try {
    const btn = document.querySelector('#register-form button');
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    btn.disabled = true;

    const res = await fetch('http://localhost:8000/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        first_name: firstName,
        last_name: lastName,
        email: email,
        password: password,
        role: "patient"
      })
    });
    
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Registration failed');
    }
    
    // Success
    successEl.innerText = 'Account created! Switching to login...';
    btn.innerHTML = 'Create Account <i class="fas fa-user-plus"></i>';
    btn.disabled = false;
    
    setTimeout(() => {
      switchAuthTab('login');
      document.getElementById('login-email').value = email;
    }, 2000);
    
  } catch (err) {
    errorEl.innerText = err.message;
    const btn = document.querySelector('#register-form button');
    btn.innerHTML = 'Create Account <i class="fas fa-user-plus"></i>';
    btn.disabled = false;
  }
}

// Update UI based on auth state
document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem('medicare_token');
  if (token) {
    const ctaDivs = document.querySelectorAll('.nav-cta');
    ctaDivs.forEach(cta => {
      cta.innerHTML = `
        <button class="btn-outline" onclick="logout()">Logout</button>
        <button class="btn-primary" onclick="location.href='patient-dashboard.html'">Dashboard</button>
      `;
    });
  }
});

function logout() {
  localStorage.removeItem('medicare_token');
  window.location.reload();
}
"""

def process():
    # append css
    with open('css/style.css', 'a', encoding='utf-8') as f:
        f.write("\\n" + css_code)
    
    # append js
    with open('js/script.js', 'a', encoding='utf-8') as f:
        f.write("\\n" + js_code)
    
    # process HTML files
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    for f in html_files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        if 'id="auth-modal"' in content:
            continue
            
        # replace sign in
        content = re.sub(r"location\.href='login\.html'", "openAuthModal('login')", content)
        content = re.sub(r'location\.href="login\.html"', "openAuthModal('login')", content)
        
        # replace register
        content = re.sub(r"location\.href='register\.html'", "openAuthModal('register')", content)
        content = re.sub(r'location\.href="register\.html"', "openAuthModal('register')", content)
        
        # append modal before </body>
        content = content.replace("</body>", modal_html + "\\n</body>")
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)

if __name__ == '__main__':
    process()
    print("Done")
