// Common interactions
document.addEventListener("DOMContentLoaded", () => {
  console.log("MediCare scripts loaded");
});

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

    const res = await fetch(`${window.MEDICARE_API_URL}/api/auth/login`, {
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

    const res = await fetch(`${window.MEDICARE_API_URL}/api/auth/register`, {
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
