import os

modal_html = """<!-- AUTH MODAL -->
<div id="auth-modal" class="auth-modal-overlay">
  <div class="auth-modal-container medicare-modal">
    <button class="auth-modal-close" onclick="closeAuthModal()"><i class="fas fa-times"></i></button>
    <div class="medicare-modal-content">
      <div class="auth-tabs-container">
        <button class="auth-tab active" onclick="switchAuthTab('login')">SIGN IN</button>
        <button class="auth-tab" onclick="switchAuthTab('register')">REGISTER</button>
      </div>
      
      <!-- Login Form -->
      <form id="login-form" class="auth-form active" onsubmit="handleLogin(event)">
        <h2 class="modal-title">Welcome <span class="text-teal">Back</span></h2>
        <p class="modal-subtitle">Enter your credentials to access your dashboard.</p>
        
        <div class="auth-field">
          <label>Email or Phone Number</label>
          <input type="email" id="login-email" required placeholder="you@example.com">
        </div>
        <div class="auth-field">
          <label>Password</label>
          <input type="password" id="login-password" required placeholder="••••••••">
          <i class="fas fa-eye password-toggle"></i>
        </div>
        
        <div class="forgot-password">
          <a href="#">Forgot Password?</a>
        </div>
        
        <button type="submit" class="submit-btn">SIGN IN</button>
        
        <div class="auth-footer">
          Don't have an account? <span class="text-teal" style="cursor:pointer;" onclick="switchAuthTab('register')">Register now</span>
        </div>
        <div id="login-error" class="auth-error"></div>
      </form>

      <!-- Register Form -->
      <form id="register-form" class="auth-form" onsubmit="handleRegister(event)">
        <h2 class="modal-title">Join <span class="text-teal">MediCare</span></h2>
        <p class="modal-subtitle">Create an account to book your appointments.</p>
        
        <div class="auth-row">
          <div class="auth-field">
            <label>First Name</label>
            <input type="text" id="register-fname" required placeholder="First">
          </div>
          <div class="auth-field">
            <label>Last Name</label>
            <input type="text" id="register-lname" required placeholder="Last">
          </div>
        </div>
        
        <div class="auth-field">
          <label>Email Address</label>
          <input type="email" id="register-email" required placeholder="you@example.com">
        </div>
        <div class="auth-field">
          <label>Password</label>
          <input type="password" id="register-password" required placeholder="••••••••">
        </div>
        
        <button type="submit" class="submit-btn">REGISTER</button>
        
        <div class="auth-footer">
          Already have an account? <span class="text-teal" style="cursor:pointer;" onclick="switchAuthTab('login')">Sign In</span>
        </div>
        <div id="register-error" class="auth-error"></div>
        <div id="register-success" class="auth-success"></div>
      </form>
    </div>
  </div>
</div>
</body>"""

css_code = """/* AUTH MODAL */
.auth-modal-overlay {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(10, 22, 40, 0.6); -webkit-backdrop-filter: blur(8px); backdrop-filter: blur(8px);
  z-index: 1000;
  opacity: 0; pointer-events: none; transition: opacity 0.3s ease;
}
.auth-modal-overlay.active { opacity: 1; pointer-events: auto; }

.auth-modal-container.medicare-modal {
  position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0.95);
  background: white; border-radius: 16px; overflow: hidden;
  width: 90%; max-width: 440px; display: flex; flex-direction: column;
  box-shadow: 0 20px 40px rgba(10, 22, 40, 0.2); border: 1px solid rgba(0,0,0,0.05);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  z-index: 1001; font-family: 'Inter', sans-serif;
}
.auth-modal-overlay.active .auth-modal-container.medicare-modal {
  transform: translate(-50%, -50%) scale(1);
}

.medicare-modal .auth-modal-close {
  position: absolute; top: 16px; right: 16px; width: 32px; height: 32px;
  background: #f0f4f8; border: none; border-radius: 50%;
  font-size: 14px; color: var(--navy); cursor: pointer;
  display: flex; align-items: center; justify-content: center; z-index: 10;
  transition: all 0.2s;
}
.medicare-modal .auth-modal-close:hover { background: #e2e8f0; color: var(--teal); }

.medicare-modal-content {
  padding: 40px 32px; display: flex; flex-direction: column; align-items: center; width: 100%;
}

.auth-tabs-container {
  display: flex; gap: 24px; margin-bottom: 24px; border-bottom: 1px solid #edf2f7; padding-bottom: 12px; width: 100%; justify-content: center; position: relative;
}
.auth-tab {
  background: none; border: none; color: #718096; font-size: 13px; font-weight: 700; cursor: pointer; padding: 5px 10px; transition: color 0.2s; position: relative; text-transform: uppercase; letter-spacing: 0.05em;
}
.auth-tab.active { color: var(--navy); }
.auth-tab.active::after {
  content: ''; position: absolute; bottom: -13px; left: 0; width: 100%; height: 3px; background: var(--teal); border-radius: 3px 3px 0 0;
}

.auth-form { width: 100%; display: none; animation: fadeIn 0.3s ease; text-align: center; }
.auth-form.active { display: block; }

.modal-title { font-size: 26px; font-family: 'Playfair Display', serif; font-weight: 700; color: var(--navy); margin-bottom: 8px; }
.text-teal { color: var(--teal); }
.modal-subtitle { font-size: 14px; color: #718096; margin-bottom: 32px; }

.auth-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

.auth-field { margin-bottom: 20px; text-align: left; position: relative; }
.auth-field label { display: block; font-size: 12px; font-weight: 600; color: var(--navy); margin-bottom: 8px; }
.auth-field input {
  width: 100%; padding: 14px 16px; border: 1px solid #e2e8f0; border-radius: 8px;
  font-size: 14px; color: #2d3748; background: #f8fafc; transition: all 0.2s; outline: none; font-family: 'Inter', sans-serif;
}
.auth-field input::placeholder { color: #a0aec0; }
.auth-field input:focus { border-color: var(--teal); background: white; box-shadow: 0 0 0 3px rgba(93, 202, 165, 0.15); }

.password-toggle { position: absolute; right: 16px; top: 35px; color: #a0aec0; cursor: pointer; font-size: 14px; transition: color 0.2s; }
.password-toggle:hover { color: var(--navy); }

.forgot-password { text-align: right; margin-bottom: 24px; margin-top: -10px; }
.forgot-password a { color: var(--teal); font-size: 12px; font-weight: 500; text-decoration: none; transition: opacity 0.2s; }
.forgot-password a:hover { opacity: 0.8; }

.submit-btn {
  width: 100%; padding: 16px; background: var(--teal); color: white; border: none; border-radius: 8px;
  font-size: 15px; font-weight: 600; cursor: pointer; transition: all 0.2s;
}
.submit-btn:hover { background: #4bb390; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(93, 202, 165, 0.3); }

.auth-footer { font-size: 13px; color: #718096; margin-top: 24px; }
.auth-footer span { font-weight: 600; transition: opacity 0.2s; }
.auth-footer span:hover { opacity: 0.8; }

.auth-error { color: #e53e3e; font-size: 13px; margin-top: 16px; text-align: center; font-weight: 500; min-height: 18px; }
.auth-success { color: #38a169; font-size: 13px; margin-top: 16px; text-align: center; font-weight: 500; min-height: 18px; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
"""

def update():
    # Update CSS
    with open('css/style.css', 'r', encoding='utf-8') as f:
        content = f.read()
    
    idx = content.find('/* AUTH MODAL */')
    if idx != -1:
        content = content[:idx] + css_code
        with open('css/style.css', 'w', encoding='utf-8') as f:
            f.write(content)

    # Update HTML
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    for f in html_files:
        with open(f, 'r', encoding='utf-8') as file:
            html = file.read()
        
        idx1 = html.find('<!-- AUTH MODAL -->')
        idx2 = html.rfind('</body>')
        
        if idx1 != -1 and idx2 != -1:
            # Also update cache buster
            html = html.replace('href="css/style.css?v=2"', 'href="css/style.css?v=3"')
            new_html = html[:idx1] + modal_html + html[idx2+7:]
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_html)

if __name__ == '__main__':
    update()
    print("Theme updated")
