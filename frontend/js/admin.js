document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem('medicare_token');
  const role = localStorage.getItem('medicare_role');

  if (!token || role !== 'admin') {
    window.location.href = 'index.html';
    return;
  }

  
  // Tab Switching Logic
  const navItems = document.querySelectorAll('.sidebar-nav .nav-item');
  const tabs = document.querySelectorAll('.admin-tab');
  const topbarTitle = document.querySelector('.topbar-title');

  navItems.forEach(item => {
    item.style.cursor = 'pointer';
    item.addEventListener('click', () => {
      // Remove active class from all
      navItems.forEach(n => n.classList.remove('active'));
      tabs.forEach(t => t.style.display = 'none');
      
      // Add active to clicked
      item.classList.add('active');
      const tabId = item.getAttribute('data-tab');
      if (tabId) {
        const tabEl = document.getElementById('tab-' + tabId);
        if (tabEl) tabEl.style.display = 'block';
      }
      
      // Update Title
      if (topbarTitle) {
        topbarTitle.innerText = item.innerText.replace(/[📅👨‍⚕️🧑‍🤝‍🧑💰🧾⚙️🔔🤖📊]/g, '').trim();
        if (tabId === 'dashboard') topbarTitle.innerText = 'Dashboard Overview';
      }
    });
  });

  // Set today's date in top bar
  const dateDisplay = document.querySelector('.date-display');
  if (dateDisplay) {
    const today = new Date();
    dateDisplay.innerText = today.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
  }

  try {
    // Fire all fetches concurrently!
    const headers = { 'Authorization': `Bearer ${token}` };
    
    const [statsRes, apptsRes, docsRes, allApptsRes, docsRes2, patRes, actRes] = await Promise.all([
      fetch(`${window.MEDICARE_API_URL}/api/admin/dashboard-stats`, { headers }).catch(e => null),
      fetch(`${window.MEDICARE_API_URL}/api/admin/appointments`, { headers }).catch(e => null),
      fetch(`${window.MEDICARE_API_URL}/api/admin/top-doctors`, { headers }).catch(e => null),
      fetch(`${window.MEDICARE_API_URL}/api/admin/all-appointments`, { headers }).catch(e => null),
      fetch(`${window.MEDICARE_API_URL}/api/admin/doctors`, { headers }).catch(e => null),
      fetch(`${window.MEDICARE_API_URL}/api/admin/patients`, { headers }).catch(e => null),
      fetch(`${window.MEDICARE_API_URL}/api/admin/recent-activity`, { headers }).catch(e => null)
    ]);

    // 1. Stats
    let stats = { total_bookings: 0, total_revenue: 0, active_doctors: 0, total_patients: 0 };
    if (statsRes && statsRes.ok) {
      stats = await statsRes.json();
      document.getElementById('stat-total-bookings').innerText = stats.total_bookings.toLocaleString();
      document.getElementById('stat-total-revenue').innerText = '$' + stats.total_revenue.toLocaleString();
      document.getElementById('stat-active-doctors').innerText = stats.active_doctors.toLocaleString();
      document.getElementById('stat-total-patients').innerText = stats.total_patients.toLocaleString();
    }

    // 2. Recent Appointments
    if (apptsRes && apptsRes.ok) {
      const appts = await apptsRes.json();
      const tbody = document.getElementById('admin-appointments-list');
      if (tbody) {
          tbody.innerHTML = '';
          appts.forEach(a => {
            let statusClass = 'status-pending';
            if (a.status === 'confirmed') statusClass = 'status-confirmed';
            if (a.status === 'cancelled') statusClass = 'status-cancelled';
            tbody.innerHTML += `
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
          if (appts.length === 0) tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:20px;">No recent appointments found.</td></tr>';
          
          const pag = document.getElementById('admin-appointments-pagination');
          if (pag) {
            pag.innerHTML = `<span>Showing ${appts.length} of ${stats.total_bookings} appointments</span>
              <div class="page-btns">
                <div class="pb active">1</div>
                <div class="pb">2</div>
                <div class="pb">3</div>
                <div class="pb">›</div>
              </div>`;
          }
      }
    }

    // 3. Top Doctors
    if (docsRes && docsRes.ok) {
      const topDocs = await docsRes.json();
      const topDocsContainer = document.getElementById('top-doctors-list');
      if (topDocsContainer) {
        topDocsContainer.innerHTML = '<div style="font-size:14px;font-weight:600;margin-bottom:16px">Top Performing Doctors</div>';
        topDocs.forEach((d, i) => {
          const colors = ['#0D9B76', '#185FA5', '#0F6E56', '#D85A30', '#7B1FA2'];
          const color = colors[i % colors.length];
          topDocsContainer.innerHTML += `
            <div class="doctor-row-item">
              <div class="mini-avatar" style="background:${color};width:36px;height:36px;font-size:12px">${d.initials}</div>
              <div class="dr-info"><div class="dr-name">${d.name}</div><div class="dr-spec">${d.specialty}</div></div>
              <div><div class="dr-rating">★ ${d.rating}</div><div class="dr-bookings">${d.bookings} bookings</div></div>
            </div>
          `;
        });
        if (topDocs.length === 0) topDocsContainer.innerHTML += '<div style="padding:10px;text-align:center;color:#666;">No bookings yet.</div>';
      }
    }

    // 4. All Appointments
    if (allApptsRes && allApptsRes.ok) {
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

    // 5. All Doctors (Grid)
    if (docsRes2 && docsRes2.ok) {
      const docs = await docsRes2.json();
      const grid = document.getElementById('admin-doctors-grid');
      if (grid) {
        grid.innerHTML = '';
        docs.forEach(d => {
          grid.innerHTML += `
            <div class="doctor-card" style="border:1px solid #E5E7EB; border-radius:12px; padding:20px; background:#fff; box-shadow:0 2px 8px rgba(0,0,0,0.02); cursor:pointer; transition:transform 0.2s;" onclick='openDoctorProfile(${JSON.stringify(d).replace(/'/g, "&#39;")})' onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform='translateY(0)'">
              <div style="display:flex; align-items:center; gap:15px; margin-bottom:15px;">
                ${d.avatar_url ? `<img src="${d.avatar_url.startsWith('http') ? d.avatar_url : window.MEDICARE_API_URL + d.avatar_url}" onerror="this.onerror=null; this.style.display='none'; this.nextElementSibling.style.display='flex';" style="width:50px; height:50px; border-radius:50%; object-fit:cover; object-position:center;"><div class="mini-avatar" style="width:50px; height:50px; font-size:16px; background:#185FA5; display:none;">${d.name.substring(4, 6).toUpperCase()}</div>` : `<div class="mini-avatar" style="width:50px; height:50px; font-size:16px; background:#185FA5;">${d.name.substring(4, 6).toUpperCase()}</div>`}
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
            </div>
          `;
        });
        if (docs.length === 0) grid.innerHTML = '<div style="grid-column: 1 / -1; padding:20px; text-align:center;">No doctors found.</div>';
      }
    }

    // 6. Patients
    if (patRes && patRes.ok) {
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

    // 7. Recent Activity
    if (actRes && actRes.ok) {
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

    // Update Sidebar Badges
    const badge = document.getElementById('sidebar-appts-badge');
    if (badge && stats.total_bookings > 0) {
      badge.innerText = stats.total_bookings;
      badge.style.display = 'inline-block';
    }

  } catch (err) {
    console.error(err);
  }
});


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
      body: JSON.stringify({ first_name: fname, last_name: lname, password: document.getElementById('admin-password').value || undefined })
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
  
  av.onerror = function() {
    av.style.display = 'none';
    ini.style.display = 'flex';
    ini.innerText = d.name.substring(4, 6).toUpperCase();
  };

  if (d.avatar_url) {
    av.src = d.avatar_url.startsWith('http') ? d.avatar_url : window.MEDICARE_API_URL + d.avatar_url;
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
