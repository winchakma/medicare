import re

file_path = r"c:\Users\user\Desktop\doctor\frontend\admin.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Settings tab
old_settings_form = """        <form id="admin-settings-form" onsubmit="handleAdminSettings(event)">
          <div style="margin-bottom: 20px;">
            <label style="display:block; margin-bottom:8px; font-weight:500;">First Name</label>
            <input type="text" id="admin-fname" class="search-input" style="width:100%; border:1px solid #E5E7EB;" required>
          </div>
          <div style="margin-bottom: 20px;">
            <label style="display:block; margin-bottom:8px; font-weight:500;">Last Name</label>
            <input type="text" id="admin-lname" class="search-input" style="width:100%; border:1px solid #E5E7EB;" required>
          </div>
          <button type="submit" class="submit-btn" style="width:auto; padding: 10px 24px;">Save Changes</button>
          <div id="settings-msg" style="margin-top: 10px; font-size: 14px;"></div>
        </form>"""

new_settings_form = """        <div style="margin-bottom:30px; display:flex; align-items:center; gap:20px;">
          <div id="admin-settings-avatar-preview" class="user-avatar" style="width:80px; height:80px; font-size:24px; cursor:pointer;" onclick="document.getElementById('admin-avatar-input').click()"></div>
          <div>
            <div style="font-weight:600; margin-bottom:8px;">Profile Picture</div>
            <div style="font-size:13px; color:var(--gray-500); margin-bottom:10px;">Click the avatar to upload a new image.</div>
            <input type="file" id="admin-avatar-input" style="display:none;" accept="image/*" onchange="handleAdminAvatarUpload(event)">
            <div id="avatar-msg" style="font-size:13px;"></div>
          </div>
        </div>
        <form id="admin-settings-form" onsubmit="handleAdminSettings(event)">
          <div style="margin-bottom: 20px;">
            <label style="display:block; margin-bottom:8px; font-weight:500;">First Name</label>
            <input type="text" id="admin-fname" class="search-input" style="width:100%; border:1px solid #E5E7EB;" required>
          </div>
          <div style="margin-bottom: 20px;">
            <label style="display:block; margin-bottom:8px; font-weight:500;">Last Name</label>
            <input type="text" id="admin-lname" class="search-input" style="width:100%; border:1px solid #E5E7EB;" required>
          </div>
          <div style="margin-bottom: 20px;">
            <label style="display:block; margin-bottom:8px; font-weight:500;">New Password <span style="font-size:12px; font-weight:normal; color:#6b7280;">(Leave blank to keep current)</span></label>
            <input type="password" id="admin-password" class="search-input" style="width:100%; border:1px solid #E5E7EB;" placeholder="••••••••">
          </div>
          <button type="submit" class="submit-btn" style="width:auto; padding: 10px 24px;">Save Changes</button>
          <div id="settings-msg" style="margin-top: 10px; font-size: 14px;"></div>
        </form>"""

html = html.replace(old_settings_form, new_settings_form)

# 2. Add tab-doctor-profile right before <!-- END content -->
doctor_profile_html = """
    <div id="tab-doctor-profile" class="admin-tab" style="display:none;">
      <div style="margin-bottom:20px;">
        <button class="filter-btn" onclick="document.querySelector('[data-tab=\\'doctors\\']').click()">← Back to Directory</button>
      </div>
      <div class="table-card" style="padding:40px; display:flex; gap:40px;">
        <div style="width:200px; text-align:center;">
          <img id="dp-avatar" src="" style="width:200px; height:200px; border-radius:12px; object-fit:cover; background:#f3f4f6; display:none;">
          <div id="dp-initials" style="width:200px; height:200px; border-radius:12px; background:var(--teal); color:white; display:flex; align-items:center; justify-content:center; font-size:64px; font-weight:600;"></div>
          <div style="margin-top:15px;">
            <span id="dp-verified" class="status-badge status-confirmed">Verified</span>
          </div>
        </div>
        <div style="flex:1;">
          <h2 id="dp-name" style="font-size:32px; color:var(--navy); margin-bottom:5px;">Loading...</h2>
          <div id="dp-specialty" style="font-size:18px; color:var(--teal); font-weight:500; margin-bottom:20px;">Specialty</div>
          
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:30px;">
            <div>
              <div style="font-size:13px; color:var(--gray-500); margin-bottom:4px;">Email Address</div>
              <div id="dp-email" style="font-weight:500; color:var(--navy);">...</div>
            </div>
            <div>
              <div style="font-size:13px; color:var(--gray-500); margin-bottom:4px;">Phone Number</div>
              <div id="dp-phone" style="font-weight:500; color:var(--navy);">...</div>
            </div>
            <div>
              <div style="font-size:13px; color:var(--gray-500); margin-bottom:4px;">Experience</div>
              <div id="dp-experience" style="font-weight:500; color:var(--navy);">...</div>
            </div>
            <div>
              <div style="font-size:13px; color:var(--gray-500); margin-bottom:4px;">Consultation Fee</div>
              <div id="dp-fee" style="font-weight:500; color:var(--navy);">...</div>
            </div>
            <div style="grid-column: 1 / -1;">
              <div style="font-size:13px; color:var(--gray-500); margin-bottom:4px;">Clinic Location</div>
              <div id="dp-location" style="font-weight:500; color:var(--navy);">...</div>
            </div>
          </div>
          
          <div style="border-top:1px solid #E5E7EB; padding-top:20px;">
            <h3 style="font-size:18px; color:var(--navy); margin-bottom:10px;">Biography</h3>
            <p id="dp-bio" style="color:var(--gray-600); line-height:1.6;">...</p>
          </div>
        </div>
      </div>
    </div>
"""
if "id=\"tab-doctor-profile\"" not in html:
    html = html.replace('  </div> <!-- END content -->', doctor_profile_html + '\n  </div> <!-- END content -->')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated admin.html")

# 3. Update admin.js
js_path = r"c:\Users\user\Desktop\doctor\frontend\js\admin.js"
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

# Update doctor render logic
old_doctor_render = """              <div class="doctor-card" style="border:1px solid #E5E7EB; border-radius:12px; padding:20px; background:#fff; box-shadow:0 2px 8px rgba(0,0,0,0.02);">
                <div style="display:flex; align-items:center; gap:15px; margin-bottom:15px;">
                  <div class="mini-avatar" style="width:50px; height:50px; font-size:16px; background:#185FA5;">${d.name.substring(4, 6).toUpperCase()}</div>
                  <div>
                    <h3 style="font-size:16px; font-weight:600; color:var(--navy); margin:0;">${d.name}</h3>
                    <div style="font-size:13px; color:var(--gray-500);">${d.specialty}</div>
                  </div>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:15px; font-size:13px;">
                  <div><strong>Email:</strong><br>${d.email}</div>
                  <div><strong>Fee:</strong><br>$${d.fee}</div>
                </div>
                <div style="display:flex; gap:10px;">
                  <button class="act-btn" style="flex:1;">Edit Profile</button>
                </div>
              </div>"""

new_doctor_render = """              <div class="doctor-card" style="border:1px solid #E5E7EB; border-radius:12px; padding:20px; background:#fff; box-shadow:0 2px 8px rgba(0,0,0,0.02); cursor:pointer; transition:transform 0.2s;" onclick='openDoctorProfile(${JSON.stringify(d).replace(/'/g, "&#39;")})' onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="display:flex; align-items:center; gap:15px; margin-bottom:15px;">
                  ${d.avatar_url ? `<img src="${window.MEDICARE_API_URL}${d.avatar_url}" style="width:50px; height:50px; border-radius:50%; object-fit:cover;">` : `<div class="mini-avatar" style="width:50px; height:50px; font-size:16px; background:#185FA5;">${d.name.substring(4, 6).toUpperCase()}</div>`}
                  <div>
                    <h3 style="font-size:16px; font-weight:600; color:var(--navy); margin:0;">${d.name}</h3>
                    <div style="font-size:13px; color:var(--gray-500);">${d.specialty}</div>
                  </div>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:15px; font-size:13px;">
                  <div><strong>Email:</strong><br>${d.email}</div>
                  <div><strong>Fee:</strong><br>$${d.fee}</div>
                </div>
                <div style="display:flex; gap:10px;">
                  <button class="act-btn" style="flex:1;">View Profile</button>
                </div>
              </div>"""

js = js.replace(old_doctor_render, new_doctor_render)

# Update settings logic
old_settings_js = """    body: JSON.stringify({ first_name: fname, last_name: lname })"""
new_settings_js = """    body: JSON.stringify({ first_name: fname, last_name: lname, password: document.getElementById('admin-password').value || undefined })"""
js = js.replace(old_settings_js, new_settings_js)

# Add new JS functions
new_functions = """
window.openDoctorProfile = function(d) {
  // Hide all tabs
  document.querySelectorAll('.admin-tab').forEach(t => t.style.display = 'none');
  // Remove active from navs
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  // Make doctor nav active
  document.querySelector('[data-tab="doctors"]').classList.add('active');
  
  // Show profile tab
  document.getElementById('tab-doctor-profile').style.display = 'block';
  
  // Populate
  document.getElementById('dp-name').innerText = d.name;
  document.getElementById('dp-specialty').innerText = d.specialty;
  document.getElementById('dp-email').innerText = d.email;
  document.getElementById('dp-phone').innerText = d.phone || 'N/A';
  document.getElementById('dp-experience').innerText = d.experience + ' years';
  document.getElementById('dp-fee').innerText = '$' + d.fee;
  document.getElementById('dp-location').innerText = d.location || 'N/A';
  document.getElementById('dp-bio').innerText = d.bio || 'No biography provided.';
  
  if (d.verified) {
    document.getElementById('dp-verified').innerText = 'Verified';
    document.getElementById('dp-verified').className = 'status-badge status-confirmed';
  } else {
    document.getElementById('dp-verified').innerText = 'Unverified';
    document.getElementById('dp-verified').className = 'status-badge status-cancelled';
  }
  
  const av = document.getElementById('dp-avatar');
  const ini = document.getElementById('dp-initials');
  if (d.avatar_url) {
    av.src = window.MEDICARE_API_URL + d.avatar_url;
    av.style.display = 'block';
    ini.style.display = 'none';
  } else {
    av.style.display = 'none';
    ini.style.display = 'flex';
    ini.innerText = d.name.substring(4, 6).toUpperCase();
  }
}

window.handleAdminAvatarUpload = async function(e) {
  const file = e.target.files[0];
  if (!file) return;
  
  const msg = document.getElementById('avatar-msg');
  msg.innerText = "Uploading...";
  msg.style.color = "var(--gray-500)";
  
  const fd = new FormData();
  fd.append("file", file);
  
  try {
    const res = await fetch(`${window.MEDICARE_API_URL}/api/admin/upload-avatar`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('medicare_token')}`
      },
      body: fd
    });
    if (res.ok) {
      const data = await res.json();
      msg.innerText = "Avatar updated!";
      msg.style.color = "green";
      document.querySelector('.user-avatar').style.backgroundImage = `url('${window.MEDICARE_API_URL}${data.avatar_url}')`;
      document.querySelector('.user-avatar').style.backgroundSize = 'cover';
      document.querySelector('.user-avatar').innerText = '';
      
      const pv = document.getElementById('admin-settings-avatar-preview');
      if(pv) {
         pv.style.backgroundImage = `url('${window.MEDICARE_API_URL}${data.avatar_url}')`;
         pv.style.backgroundSize = 'cover';
         pv.innerText = '';
      }
    } else {
      msg.innerText = "Upload failed.";
      msg.style.color = "red";
    }
  } catch(err) {
    msg.innerText = "Upload error.";
    msg.style.color = "red";
  }
}

// In the dashboard init, check if we need to show the avatar
setTimeout(async () => {
  const token = localStorage.getItem('medicare_token');
  try {
     const meRes = await fetch(`${window.MEDICARE_API_URL}/api/auth/me`, {
       headers: { 'Authorization': `Bearer ${token}` }
     });
     if (meRes.ok) {
        const me = await meRes.json();
        const av = document.querySelector('.user-avatar');
        const pv = document.getElementById('admin-settings-avatar-preview');
        if (me.avatar_url) {
           av.style.backgroundImage = `url('${window.MEDICARE_API_URL}${me.avatar_url}')`;
           av.style.backgroundSize = 'cover';
           av.innerText = '';
           if(pv) {
             pv.style.backgroundImage = `url('${window.MEDICARE_API_URL}${me.avatar_url}')`;
             pv.style.backgroundSize = 'cover';
             pv.innerText = '';
           }
        } else {
           if(pv) pv.innerText = me.first_name[0] + me.last_name[0];
        }
     }
  } catch(e) {}
}, 500);
"""

if "window.openDoctorProfile" not in js:
    js += "\n" + new_functions

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)

print("Updated admin.js")
