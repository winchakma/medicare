import os

modal_html = """<!-- AUTH MODAL -->
<div id="auth-modal" class="auth-modal-overlay">
  <div class="auth-modal-container dark-modal">
    <button class="auth-modal-close" onclick="closeAuthModal()"><i class="fas fa-times"></i></button>
    <div class="dark-modal-content">
      <div class="dark-auth-tabs">
        <button class="auth-tab dark-auth-tab active" onclick="switchAuthTab('login')">SIGN IN</button>
        <button class="auth-tab dark-auth-tab" onclick="switchAuthTab('register')">REGISTER</button>
      </div>
      
      <!-- Login Form -->
      <form id="login-form" class="auth-form active" onsubmit="handleLogin(event)">
        <h2 class="dark-modal-title">WELCOME <span class="text-yellow">BACK</span></h2>
        <p class="dark-modal-subtitle">Enter your elite credentials to continue.</p>
        
        <div class="dark-auth-field">
          <label>Email or Phone Number</label>
          <input type="email" id="login-email" required placeholder="you@example.com or +880...">
        </div>
        <div class="dark-auth-field">
          <label>Password</label>
          <input type="password" id="login-password" required placeholder="••••••••">
          <i class="fas fa-eye password-toggle"></i>
        </div>
        
        <div class="forgot-password">
          <a href="#">Forgot Password?</a>
        </div>
        
        <button type="submit" class="dark-submit-btn">SIGN IN</button>
        
        <div class="dark-auth-footer">
          Don't have an account? <span class="text-yellow" style="cursor:pointer;" onclick="switchAuthTab('register')">Join the Elite</span>
        </div>
        <div id="login-error" class="auth-error"></div>
      </form>

      <!-- Register Form -->
      <form id="register-form" class="auth-form" onsubmit="handleRegister(event)">
        <h2 class="dark-modal-title">JOIN <span class="text-yellow">THE ELITE</span></h2>
        <p class="dark-modal-subtitle">Create an account to book your appointments.</p>
        
        <div class="dark-auth-row">
          <div class="dark-auth-field">
            <label>First Name</label>
            <input type="text" id="register-fname" required placeholder="First">
          </div>
          <div class="dark-auth-field">
            <label>Last Name</label>
            <input type="text" id="register-lname" required placeholder="Last">
          </div>
        </div>
        
        <div class="dark-auth-field">
          <label>Email Address</label>
          <input type="email" id="register-email" required placeholder="you@example.com">
        </div>
        <div class="dark-auth-field">
          <label>Password</label>
          <input type="password" id="register-password" required placeholder="••••••••">
        </div>
        
        <button type="submit" class="dark-submit-btn">REGISTER</button>
        
        <div class="dark-auth-footer">
          Already have an account? <span class="text-yellow" style="cursor:pointer;" onclick="switchAuthTab('login')">Sign In</span>
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
  background: rgba(0, 0, 0, 0.85); backdrop-filter: blur(8px);
  z-index: 1000; display: flex; align-items: center; justify-content: center;
  opacity: 0; pointer-events: none; transition: opacity 0.3s ease;
}
.auth-modal-overlay.active { opacity: 1; pointer-events: auto; }

.auth-modal-container.dark-modal {
  background: #0f0f11; border-radius: 12px; overflow: hidden;
  width: 90%; max-width: 460px; display: flex; flex-direction: column;
  box-shadow: 0 24px 60px rgba(0,0,0,0.8); border: 1px solid #222;
  transform: translateY(30px) scale(0.95); transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
}
.auth-modal-overlay.active .auth-modal-container.dark-modal {
  transform: translateY(0) scale(1);
}

.dark-modal .auth-modal-close {
  position: absolute; top: 20px; right: 20px; width: 32px; height: 32px;
  background: #1a1a1a; border: 1px solid #333; border-radius: 50%;
  font-size: 14px; color: #fde047; cursor: pointer;
  display: flex; align-items: center; justify-content: center; z-index: 10;
  transition: all 0.2s;
}
.dark-modal .auth-modal-close:hover { background: #333; color: white; border-color: #fde047; }

.dark-modal-content {
  padding: 48px 40px; display: flex; flex-direction: column; align-items: center; width: 100%;
}

.dark-auth-tabs {
  display: flex; gap: 24px; margin-bottom: 32px; border-bottom: 1px solid #222; padding-bottom: 12px; width: 100%; justify-content: center; position: relative;
}
.dark-auth-tab {
  background: none; border: none; color: #555; font-size: 11px; font-weight: 800; letter-spacing: 0.1em; cursor: pointer; padding: 5px 10px; transition: color 0.2s; position: relative; text-transform: uppercase;
}
.dark-auth-tab.active { color: #fde047; }
.dark-auth-tab.active::after {
  content: ''; position: absolute; bottom: -13px; left: 0; width: 100%; height: 2px; background: #fde047;
}

.auth-form { width: 100%; display: none; animation: fadeIn 0.3s ease; text-align: center; }
.auth-form.active { display: block; }

.dark-modal-title { font-size: 28px; font-weight: 800; color: white; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; font-family: 'Inter', sans-serif; }
.text-yellow { color: #fde047; }
.dark-modal-subtitle { font-size: 13px; color: #666; margin-bottom: 32px; }

.dark-auth-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

.dark-auth-field { margin-bottom: 20px; text-align: left; position: relative; }
.dark-auth-field label { display: block; font-size: 10px; font-weight: 700; color: #666; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em; }
.dark-auth-field input {
  width: 100%; padding: 14px 16px; border: 1px solid #222; border-radius: 8px;
  font-size: 13px; color: white; background: #161618; transition: all 0.2s; outline: none; font-family: 'Inter', sans-serif;
}
.dark-auth-field input::placeholder { color: #444; font-style: italic; }
.dark-auth-field input:focus { border-color: #fde047; background: #1a1a1c; box-shadow: 0 0 0 1px rgba(253,224,71,0.2); }

.password-toggle { position: absolute; right: 16px; top: 35px; color: #f26522; cursor: pointer; font-size: 14px; }

.forgot-password { text-align: right; margin-bottom: 24px; margin-top: -10px; }
.forgot-password a { color: #555; font-size: 11px; text-decoration: none; transition: color 0.2s; }
.forgot-password a:hover { color: white; }

.dark-submit-btn {
  width: 100%; padding: 16px; background: #fde047; color: #000; border: none; border-radius: 8px;
  font-size: 14px; font-weight: 800; letter-spacing: 0.05em; cursor: pointer; transition: all 0.2s; text-transform: uppercase;
}
.dark-submit-btn:hover { background: #eab308; }

.dark-auth-footer { font-size: 12px; color: #555; margin-top: 24px; }
.dark-auth-footer span { font-weight: 700; transition: color 0.2s; }
.dark-auth-footer span:hover { color: white; }

.auth-error { color: #ef4444; font-size: 13px; margin-top: 12px; text-align: center; font-weight: 500; min-height: 18px; }
.auth-success { color: #22c55e; font-size: 13px; margin-top: 12px; text-align: center; font-weight: 500; min-height: 18px; }
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
            new_html = html[:idx1] + modal_html + html[idx2+7:]
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_html)

if __name__ == '__main__':
    update()
    print("Update complete")
