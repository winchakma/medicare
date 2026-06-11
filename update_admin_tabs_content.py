import re

html_path = r"c:\Users\user\Desktop\doctor\frontend\admin.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Replace the content of the other tabs
new_appointments_tab = """
    <div id="tab-appointments" class="admin-tab" style="display:none;">
      <div class="table-card">
        <div class="table-header">
          <div class="table-title">All Appointments</div>
        </div>
        <table>
          <thead>
            <tr>
              <th>Booking ID</th>
              <th>Patient</th>
              <th>Doctor</th>
              <th>Specialty</th>
              <th>Date & Time</th>
              <th>Fee</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody id="all-appointments-list"><tr><td colspan="8" style="text-align:center;padding:20px;">Loading appointments...</td></tr></tbody>
        </table>
      </div>
    </div>
"""

new_doctors_tab = """
    <div id="tab-doctors" class="admin-tab" style="display:none;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 20px;">
        <h2 style="font-size:20px; font-weight:600; color:var(--navy);">Doctors Directory</h2>
        <button class="add-btn">+ Add Doctor</button>
      </div>
      <div class="doctors-grid" id="admin-doctors-grid" style="display:grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;">
        <div style="padding:20px; text-align:center; grid-column: 1 / -1;">Loading doctors...</div>
      </div>
    </div>
"""

new_patients_tab = """
    <div id="tab-patients" class="admin-tab" style="display:none;">
      <div class="table-card">
        <div class="table-header">
          <div class="table-title">Registered Patients</div>
        </div>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Joined Date</th>
            </tr>
          </thead>
          <tbody id="admin-patients-list"><tr><td colspan="5" style="text-align:center;padding:20px;">Loading patients...</td></tr></tbody>
        </table>
      </div>
    </div>
"""

new_settings_tab = """
    <div id="tab-settings" class="admin-tab" style="display:none;">
      <div class="table-card" style="max-width: 600px; padding: 30px;">
        <h2 style="font-size:20px; font-weight:600; color:var(--navy); margin-bottom: 20px;">Profile Settings</h2>
        <form id="admin-settings-form" onsubmit="handleAdminSettings(event)">
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
        </form>
      </div>
    </div>
"""

# Replace the old tabs in HTML
html = re.sub(r'<div id="tab-appointments".*?</div>\s*(?=<div id="tab-doctors")', new_appointments_tab, html, flags=re.DOTALL)
html = re.sub(r'<div id="tab-doctors".*?</div>\s*(?=<div id="tab-patients")', new_doctors_tab, html, flags=re.DOTALL)
html = re.sub(r'<div id="tab-patients".*?</div>\s*(?=<div id="tab-revenue")', new_patients_tab, html, flags=re.DOTALL)
html = re.sub(r'<div id="tab-settings".*?</div>\s*(?=</div> <!-- END content -->)', new_settings_tab + '\n', html, flags=re.DOTALL)

# Add recent activity container to dashboard
recent_activity_new = """
      <div class="bottom-card" style="max-height: 400px; overflow-y: auto;">
        <div style="font-size:14px;font-weight:600;margin-bottom:16px">Recent Activity</div>
        <div id="admin-recent-activity">Loading activity...</div>
      </div>
"""
html = re.sub(r'<div class="bottom-card">\s*<div style="font-size:14px;font-weight:600;margin-bottom:16px">Recent Activity</div>.*?</div>', recent_activity_new, html, flags=re.DOTALL)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Updated admin HTML with real tab containers")

# Now update admin.js
js_path = r"c:\Users\user\Desktop\doctor\frontend\js\admin.js"
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

# Add the fetch logic for the new tabs
new_js_logic = """
    // 4. Fetch all appointments
    try {
      const allApptsRes = await fetch(`${window.MEDICARE_API_URL}/api/admin/all-appointments`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (allApptsRes.ok) {
        const allAppts = await allApptsRes.json();
        const allTbody = document.getElementById('all-appointments-list');
        if (allTbody) {
          allTbody.innerHTML = '';
          allAppts.forEach(a => {
            let statusClass = 'status-pending';
            if (a.status === 'confirmed') statusClass = 'status-confirmed';
            if (a.status === 'cancelled') statusClass = 'status-cancelled';
            allTbody.innerHTML += `
              <tr>
                <td style="font-weight:500;color:var(--navy)">${a.booking_id}</td>
                <td>${a.patient_name}</td>
                <td><div class="doc-cell"><div class="mini-avatar" style="background:#0D9B76">${a.doctor_initials}</div>${a.doctor_name}</div></td>
                <td>${a.specialty}</td>
                <td>${a.date} &middot; ${a.time_slot}</td>
                <td style="font-weight:500">$${a.fee}</td>
                <td><span class="status-badge ${statusClass}">${a.status}</span></td>
                <td><div class="action-btns"><button class="act-btn">View</button></div></td>
              </tr>
            `;
          });
          if (allAppts.length === 0) allTbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:20px;">No appointments found.</td></tr>';
        }
      }
    } catch(e) {}

    // 5. Fetch Doctors
    try {
      const docsRes = await fetch(`${window.MEDICARE_API_URL}/api/admin/doctors`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (docsRes.ok) {
        const docs = await docsRes.json();
        const grid = document.getElementById('admin-doctors-grid');
        if (grid) {
          grid.innerHTML = '';
          docs.forEach(d => {
            grid.innerHTML += `
              <div class="doctor-card" style="border:1px solid #E5E7EB; border-radius:12px; padding:20px; background:#fff; box-shadow:0 2px 8px rgba(0,0,0,0.02);">
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
              </div>
            `;
          });
          if (docs.length === 0) grid.innerHTML = '<div style="grid-column: 1 / -1; padding:20px; text-align:center;">No doctors found.</div>';
        }
      }
    } catch(e) {}

    // 6. Fetch Patients
    try {
      const patRes = await fetch(`${window.MEDICARE_API_URL}/api/admin/patients`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (patRes.ok) {
        const pats = await patRes.json();
        const ptbody = document.getElementById('admin-patients-list');
        if (ptbody) {
          ptbody.innerHTML = '';
          pats.forEach(p => {
            const dateStr = new Date(p.created_at).toLocaleDateString();
            ptbody.innerHTML += `
              <tr>
                <td style="color:var(--navy); font-weight:500;">${p.id.substring(0, 8)}...</td>
                <td>${p.name}</td>
                <td>${p.email}</td>
                <td>${p.phone}</td>
                <td>${dateStr}</td>
              </tr>
            `;
          });
          if (pats.length === 0) ptbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:20px;">No patients found.</td></tr>';
        }
      }
    } catch(e) {}

    // 7. Fetch Recent Activity
    try {
      const actRes = await fetch(`${window.MEDICARE_API_URL}/api/admin/recent-activity`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (actRes.ok) {
        const acts = await actRes.json();
        const actDiv = document.getElementById('admin-recent-activity');
        if (actDiv) {
          actDiv.innerHTML = '';
          acts.forEach(a => {
            actDiv.innerHTML += `
              <div class="activity-item">
                <div class="activity-dot" style="background:${a.color}"></div>
                <div>
                  <div class="activity-text">${a.text}</div>
                  <div class="activity-time">${a.time_str}</div>
                </div>
              </div>
            `;
          });
          if (acts.length === 0) actDiv.innerHTML = '<div style="padding:10px;text-align:center;color:#666;">No recent activity.</div>';
        }
      }
    } catch(e) {}

    // Update Sidebar Badges
    const badge = document.getElementById('sidebar-appts-badge');
    if (badge && stats.total_bookings > 0) {
      badge.innerText = stats.total_bookings;
      badge.style.display = 'inline-block';
    }
"""

js = js.replace('  } catch (err) {', new_js_logic + '\n  } catch (err) {')

settings_fn = """
async function handleAdminSettings(e) {
  e.preventDefault();
  const fname = document.getElementById('admin-fname').value;
  const lname = document.getElementById('admin-lname').value;
  const msg = document.getElementById('settings-msg');
  
  try {
    const res = await fetch(`${window.MEDICARE_API_URL}/api/admin/settings`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('medicare_token')}`
      },
      body: JSON.stringify({ first_name: fname, last_name: lname })
    });
    if (res.ok) {
      msg.innerText = "Profile updated successfully!";
      msg.style.color = "green";
      // Update sidebar name
      document.querySelector('.user-name').innerText = fname + ' ' + lname;
      document.querySelector('.user-avatar').innerText = fname[0] + lname[0];
    } else {
      msg.innerText = "Failed to update profile.";
      msg.style.color = "red";
    }
  } catch(e) {
    msg.innerText = "Error updating profile.";
    msg.style.color = "red";
  }
}
"""

js += "\n" + settings_fn

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)

print("Updated admin.js")
