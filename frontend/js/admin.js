document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem('medicare_token');
  const role = localStorage.getItem('medicare_role');

  if (!token || role !== 'admin') {
    window.location.href = 'index.html';
    return;
  }

  // Doctor Initials Helper
  window.getDoctorInitials = function(name) {
    if (!name) return 'DR';
    const cleanName = name.replace(/^Dr\.\s+/i, '').trim();
    const parts = cleanName.split(/\s+/);
    if (parts.length >= 2) {
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }
    return cleanName.substring(0, 2).toUpperCase();
  };

  // Add Add-Doctor Click Listeners
  const addDocBtns = document.querySelectorAll('.add-btn');
  addDocBtns.forEach(btn => {
    btn.style.cursor = 'pointer';
    btn.addEventListener('click', () => {
      openAddDoctorModal();
    });
  });

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

  // Appointments filter state
  window.recentAppointments = [];
  window.currentRecentPage = 1;
  window.recentPageSize = 5;
  window.currentStatusFilter = 'all';
  window.searchQuery = '';

  window.renderRecentAppointmentsTable = function() {
    const tbody = document.getElementById('admin-appointments-list');
    if (!tbody) return;
    tbody.innerHTML = '';
    
    // Filter
    let filtered = [...window.recentAppointments];
    if (window.currentStatusFilter !== 'all') {
      filtered = filtered.filter(a => a.status === window.currentStatusFilter);
    }
    if (window.searchQuery) {
      const q = window.searchQuery.toLowerCase();
      filtered = filtered.filter(a => 
        a.booking_id.toLowerCase().includes(q) ||
        a.patient_name.toLowerCase().includes(q) ||
        a.doctor_name.toLowerCase().includes(q) ||
        a.specialty.toLowerCase().includes(q)
      );
    }

    const startIndex = (window.currentRecentPage - 1) * window.recentPageSize;
    const endIndex = startIndex + window.recentPageSize;
    const pageAppts = filtered.slice(startIndex, endIndex);
    
    pageAppts.forEach(a => {
      let statusClass = 'status-pending';
      if (a.status === 'confirmed') statusClass = 'status-confirmed';
      if (a.status === 'cancelled') statusClass = 'status-cancelled';
      tbody.innerHTML += `
        <tr>
          <td style="font-weight:500;color:var(--navy)">${a.booking_id}</td>
          <td>${a.patient_name}</td>
          <td><div class="doc-cell"><div class="mini-avatar" style="background:#0D9B76">${window.getDoctorInitials(a.doctor_name)}</div>${a.doctor_name}</div></td>
          <td>${a.specialty}</td>
          <td>${a.date} &middot; ${a.time_slot}</td>
          <td style="font-weight:500">$${a.fee}</td>
          <td><span class="status-badge ${statusClass}">${a.status}</span></td>
          <td><div class="action-btns"><button class="act-btn" onclick="openDoctorProfileByAppt('${a.doctor_name}')">View</button></div></td>
        </tr>
      `;
    });
    
    if (filtered.length === 0) {
      tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:20px;">No appointments found.</td></tr>';
    }
    
    // Update pagination UI
    const pag = document.getElementById('admin-appointments-pagination');
    if (pag) {
      const total = filtered.length;
      const totalPages = Math.ceil(total / window.recentPageSize) || 1;
      
      let pageBtnsHTML = '';
      for (let p = 1; p <= totalPages; p++) {
        pageBtnsHTML += `<div class="pb ${p === window.currentRecentPage ? 'active' : ''}" onclick="changeRecentPage(${p})">${p}</div>`;
      }
      if (totalPages > 1 && window.currentRecentPage < totalPages) {
        pageBtnsHTML += `<div class="pb" onclick="changeRecentPage(${window.currentRecentPage + 1})">›</div>`;
      }
      
      pag.innerHTML = `
        <span>Showing ${total > 0 ? startIndex + 1 : 0}-${Math.min(endIndex, total)} of ${total} appointments</span>
        <div class="page-btns">
          ${pageBtnsHTML}
        </div>
      `;
    }
  };

  window.changeRecentPage = function(page) {
    window.currentRecentPage = page;
    window.renderRecentAppointmentsTable();
  };

  window.openDoctorProfileByAppt = function(docName) {
    if (window.allDoctorsMap) {
      const doc = Object.values(window.allDoctorsMap).find(d => d.name === docName);
      if (doc) {
        window.openDoctorProfile(doc.id);
      }
    }
  };

  // Wire search input
  const searchInput = document.querySelector('.search-input');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      window.searchQuery = e.target.value;
      window.currentRecentPage = 1;
      window.renderRecentAppointmentsTable();
    });
  }

  // Wire filter button modal/dropdown
  const filterBtn = document.querySelector('.filter-btn');
  if (filterBtn) {
    filterBtn.style.position = 'relative';
    filterBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      let dropdown = document.getElementById('filter-status-dropdown');
      if (dropdown) {
        dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
      } else {
        dropdown = document.createElement('div');
        dropdown.id = 'filter-status-dropdown';
        dropdown.style.position = 'absolute';
        dropdown.style.right = '0';
        dropdown.style.top = '100%';
        dropdown.style.background = '#fff';
        dropdown.style.border = '1px solid #E5E7EB';
        dropdown.style.borderRadius = '8px';
        dropdown.style.boxShadow = '0 4px 12px rgba(0,0,0,0.08)';
        dropdown.style.zIndex = '1000';
        dropdown.style.width = '140px';
        dropdown.style.padding = '8px 0';
        dropdown.style.marginTop = '4px';
        
        const statuses = ['all', 'pending', 'confirmed', 'cancelled'];
        statuses.forEach(st => {
          const item = document.createElement('div');
          item.innerText = st.charAt(0).toUpperCase() + st.slice(1);
          item.style.padding = '8px 16px';
          item.style.cursor = 'pointer';
          item.style.fontSize = '13px';
          item.style.fontWeight = window.currentStatusFilter === st ? '600' : '400';
          item.style.color = window.currentStatusFilter === st ? 'var(--teal)' : 'var(--navy)';
          item.addEventListener('mouseover', () => item.style.background = '#F9FAFB');
          item.addEventListener('mouseout', () => item.style.background = 'transparent');
          item.addEventListener('click', () => {
            window.currentStatusFilter = st;
            window.currentRecentPage = 1;
            window.renderRecentAppointmentsTable();
            dropdown.style.display = 'none';
            // Update bold item
            document.querySelectorAll('#filter-status-dropdown div').forEach(div => {
              div.style.fontWeight = '400';
              div.style.color = 'var(--navy)';
            });
            item.style.fontWeight = '600';
            item.style.color = 'var(--teal)';
          });
          dropdown.appendChild(item);
        });
        filterBtn.appendChild(dropdown);
        dropdown.style.display = 'block';
      }
    });

    document.addEventListener('click', () => {
      const dropdown = document.getElementById('filter-status-dropdown');
      if (dropdown) dropdown.style.display = 'none';
    });
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

    // 1. Stats & Dynamic Charts
    let stats = { total_bookings: 0, total_revenue: 0, active_doctors: 0, total_patients: 0, monthly_bookings: {}, specialty_distribution: {} };
    if (statsRes && statsRes.ok) {
      stats = await statsRes.json();
      document.getElementById('stat-total-bookings').innerText = stats.total_bookings.toLocaleString();
      document.getElementById('stat-total-revenue').innerText = '$' + stats.total_revenue.toLocaleString();
      document.getElementById('stat-active-doctors').innerText = stats.active_doctors.toLocaleString();
      document.getElementById('stat-total-patients').innerText = stats.total_patients.toLocaleString();

      // Dynamic Monthly Bookings bar chart scaling
      const barChart = document.querySelector('.bar-chart');
      if (barChart) {
        barChart.innerHTML = '';
        const months = [];
        const today = new Date();
        for (let i = 5; i >= 0; i--) {
          const m = new Date(today.getFullYear(), today.getMonth() - i, 1);
          months.push(m.toLocaleDateString('en-US', { month: 'short' }));
        }

        const counts = months.map(m => stats.monthly_bookings[m] || 0);
        const maxVal = Math.max(...counts, 0) || 1;

        months.forEach((m, idx) => {
          const val = stats.monthly_bookings[m] || 0;
          const pct = (val / maxVal) * 100;
          barChart.innerHTML += `
            <div class="bar-wrap">
              <div class="bar" style="height:${pct}%;background:var(--teal);opacity:${0.5 + (idx * 0.1)}"></div>
              <div class="bar-label">${m}</div>
            </div>
          `;
        });
      }

      // Dynamic Specialty Donut Chart
      const specialtyDist = stats.specialty_distribution || {};
      const specialtyTotal = Object.values(specialtyDist).reduce((a, b) => a + b, 0);
      const donutWrap = document.querySelector('.donut-wrap');
      if (donutWrap) {
        if (specialtyTotal === 0) {
          donutWrap.innerHTML = `
            <svg width="110" height="110" viewBox="0 0 110 110">
              <circle cx="55" cy="55" r="40" fill="none" stroke="#EFF1F5" stroke-width="18"/>
              <text x="55" y="60" text-anchor="middle" font-size="12" fill="#6B7280">No data</text>
            </svg>
            <div class="donut-legend">
              <div class="legend-item"><div class="legend-dot" style="background:#EFF1F5"></div> No Bookings</div>
            </div>
          `;
        } else {
          const colors = ['#0D9B76', '#185FA5', '#D85A30', '#EF9F27', '#8B5CF6', '#EC4899', '#3B82F6'];
          const entries = Object.entries(specialtyDist).sort((a, b) => b[1] - a[1]);
          
          let svgCircles = `<circle cx="55" cy="55" r="40" fill="none" stroke="#EFF1F5" stroke-width="18"/>`;
          let legendHTML = '';
          
          const circ = 251.2;
          let offset = 0;
          
          entries.forEach(([spec, count], index) => {
            const percent = (count / specialtyTotal) * 100;
            const color = colors[index % colors.length];
            const active = (count / specialtyTotal) * circ;
            const remaining = circ - active;
            
            svgCircles += `
              <circle cx="55" cy="55" r="40" fill="none" stroke="${color}" stroke-width="18" 
                stroke-dasharray="${active.toFixed(1)} ${remaining.toFixed(1)}" 
                stroke-dashoffset="${(-offset).toFixed(1)}" 
                transform="rotate(-90 55 55)"/>
            `;
            
            legendHTML += `
              <div class="legend-item"><div class="legend-dot" style="background:${color}"></div> ${spec} (${Math.round(percent)}%)</div>
            `;
            
            offset += active;
          });
          
          const topSpec = entries[0][0];
          const topSpecPercent = Math.round((entries[0][1] / specialtyTotal) * 100);
          
          donutWrap.innerHTML = `
            <svg width="110" height="110" viewBox="0 0 110 110">
              ${svgCircles}
              <text x="55" y="52" text-anchor="middle" font-size="14" font-weight="600" fill="#0A1628">${topSpecPercent}%</text>
              <text x="55" y="64" text-anchor="middle" font-size="9" fill="#6B7280">${topSpec.length > 10 ? topSpec.substring(0, 8) + '..' : topSpec}</text>
            </svg>
            <div class="donut-legend" style="max-height: 120px; overflow-y: auto;">
              ${legendHTML}
            </div>
          `;
        }
      }
    }

    // 2. Recent Appointments
    if (apptsRes && apptsRes.ok) {
      window.recentAppointments = await apptsRes.json();
      window.renderRecentAppointmentsTable();
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
              <div class="mini-avatar" style="background:${color};width:36px;height:36px;font-size:12px">${window.getDoctorInitials(d.name)}</div>
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
              <td><div class="doc-cell"><div class="mini-avatar" style="background:#0D9B76">${window.getDoctorInitials(a.doctor_name)}</div>${a.doctor_name}</div></td>
              <td>${a.specialty}</td>
              <td>${a.date} &middot; ${a.time_slot}</td>
              <td style="font-weight:500">$${a.fee}</td>
              <td><span class="status-badge ${statusClass}">${a.status}</span></td>
              <td><div class="action-btns"><button class="act-btn" onclick="openDoctorProfileByAppt('${a.doctor_name}')">View</button></div></td>
            </tr>
          `;
        });
        if (allAppts.length === 0) allTbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:20px;">No appointments found.</td></tr>';
      }
    }

    // 5. All Doctors (Grid)
    if (docsRes2 && docsRes2.ok) {
      const docs = await docsRes2.json();
      window.allDoctorsMap = {};
      docs.forEach(d => {
        window.allDoctorsMap[d.id] = d;
      });
      const grid = document.getElementById('admin-doctors-grid');
      if (grid) {
        grid.innerHTML = '';
        docs.forEach(d => {
          grid.innerHTML += `
            <div class="doctor-card" style="border:1px solid #E5E7EB; border-radius:12px; padding:20px; background:#fff; box-shadow:0 2px 8px rgba(0,0,0,0.02); cursor:pointer; transition:transform 0.2s;" onclick="openDoctorProfile('${d.id}')" onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform='translateY(0)'">
              <div style="display:flex; align-items:center; gap:15px; margin-bottom:15px;">
                ${d.avatar_url ? `<img src="${d.avatar_url.startsWith('http') ? d.avatar_url : window.MEDICARE_API_URL + d.avatar_url}" onerror="this.onerror=null; this.style.display='none'; this.nextElementSibling.style.display='flex';" style="width:50px; height:50px; border-radius:50%; object-fit:cover; object-position:center;"><div class="mini-avatar" style="width:50px; height:50px; font-size:16px; background:#185FA5; display:none;">${window.getDoctorInitials(d.name)}</div>` : `<div class="mini-avatar" style="width:50px; height:50px; font-size:16px; background:#185FA5;">${window.getDoctorInitials(d.name)}</div>`}
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
      
      // Populate admin activity timeline
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

      // Populate notification dropdown list
      const notifContainer = document.getElementById('notif-list-container');
      if (notifContainer) {
        notifContainer.innerHTML = '';
        acts.forEach(a => {
          notifContainer.innerHTML += `
            <div style="padding: 10px 16px; border-bottom: 1px solid #F9FAFB; display: flex; gap: 10px; align-items: flex-start; text-align: left;">
              <div style="width: 8px; height: 8px; border-radius: 50%; background: ${a.color}; margin-top: 5px; flex-shrink: 0;"></div>
              <div>
                <div style="font-weight: 500; line-height: 1.4; color: var(--navy);">${a.text}</div>
                <div style="font-size: 11px; color: #9CA3AF; margin-top: 2px;">${a.time_str}</div>
              </div>
            </div>
          `;
        });
        if (acts.length === 0) {
          notifContainer.innerHTML = '<div style="padding: 16px; text-align: center; color: #9CA3AF;">No new notifications</div>';
        }
      }
    } else {
      const actDiv = document.getElementById('admin-recent-activity');
      if (actDiv) actDiv.innerHTML = '<div style="padding:10px;text-align:center;color:#666;">Failed to load activity.</div>';
    }

    // Wire notification dropdown toggle
    const notifBtn = document.getElementById('notif-bell-btn');
    const notifDropdown = document.getElementById('notif-bell-dropdown');
    if (notifBtn && notifDropdown) {
      notifBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        notifDropdown.style.display = notifDropdown.style.display === 'block' ? 'none' : 'block';
        const dot = document.getElementById('notif-bell-dot');
        if (dot) dot.style.display = 'none';
      });
      document.addEventListener('click', () => {
        notifDropdown.style.display = 'none';
      });
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

window.openDoctorProfile = function(dOrId) {
  let d = dOrId;
  if (typeof dOrId === 'string' && window.allDoctorsMap) {
    d = window.allDoctorsMap[dOrId];
  }
  if (!d) return;

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

  const verifyBtn = document.getElementById('dp-verify-btn');
  const deleteBtn = document.getElementById('dp-delete-btn');
  
  if (verifyBtn) {
    verifyBtn.innerText = d.verified ? 'Unverify Doctor' : 'Verify Doctor';
    verifyBtn.onclick = async () => {
      try {
        const res = await fetch(`${window.MEDICARE_API_URL}/api/admin/doctors/${d.id}/verify`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('medicare_token')}`
          }
        });
        if (res.ok) {
          const data = await res.json();
          d.verified = data.verified;
          // Refresh UI
          window.openDoctorProfile(d);
          // Reload doctor map list when page reloads/refreshes
          if (window.allDoctorsMap && window.allDoctorsMap[d.id]) {
            window.allDoctorsMap[d.id].verified = data.verified;
          }
        }
      } catch (err) {
        console.error(err);
      }
    };
  }

  if (deleteBtn) {
    deleteBtn.onclick = async () => {
      if (confirm(`Are you sure you want to remove Dr. ${d.name.replace(/^Dr\.\s+/i, '')} permanently?`)) {
        try {
          const res = await fetch(`${window.MEDICARE_API_URL}/api/admin/doctors/${d.id}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('medicare_token')}`
            }
          });
          if (res.ok) {
            alert('Doctor deleted successfully.');
            window.location.reload();
          }
        } catch (err) {
          console.error(err);
        }
      }
    };
  }
  
  const av = document.getElementById('dp-avatar');
  const ini = document.getElementById('dp-initials');
  
  av.onerror = function() {
    av.style.display = 'none';
    ini.style.display = 'flex';
    ini.innerText = window.getDoctorInitials(d.name);
  };

  if (d.avatar_url) {
    av.src = d.avatar_url.startsWith('http') ? d.avatar_url : window.MEDICARE_API_URL + d.avatar_url;
    av.style.display = 'block';
    ini.style.display = 'none';
  } else {
    av.style.display = 'none';
    ini.style.display = 'flex';
    ini.innerText = window.getDoctorInitials(d.name);
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

// Add Doctor Modal Helpers
window.openAddDoctorModal = function() {
  let modal = document.getElementById('add-doctor-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'add-doctor-modal';
    modal.className = 'auth-modal-overlay';
    modal.style.zIndex = '9999';
    modal.innerHTML = `
      <div class="auth-modal-container medicare-modal" style="max-width:500px; padding:30px;">
        <button class="auth-modal-close" onclick="closeAddDoctorModal()"><i class="fas fa-times"></i></button>
        <h2 style="font-family:'Playfair Display',serif; color:var(--navy); font-size:24px; margin-bottom: 20px; text-align:center;">Add New Doctor</h2>
        <form id="add-doctor-form" onsubmit="handleAddDoctorSubmit(event)">
          <div style="display:flex; gap:15px; margin-bottom:15px;">
            <div style="flex:1;">
              <label style="display:block; margin-bottom:5px; font-size:13px; font-weight:500;">First Name</label>
              <input type="text" id="add-doc-fname" class="search-input" style="width:100%; border:1px solid #E5E7EB;" required placeholder="First">
            </div>
            <div style="flex:1;">
              <label style="display:block; margin-bottom:5px; font-size:13px; font-weight:500;">Last Name</label>
              <input type="text" id="add-doc-lname" class="search-input" style="width:100%; border:1px solid #E5E7EB;" required placeholder="Last">
            </div>
          </div>
          <div style="margin-bottom:15px;">
            <label style="display:block; margin-bottom:5px; font-size:13px; font-weight:500;">Email Address</label>
            <input type="email" id="add-doc-email" class="search-input" style="width:100%; border:1px solid #E5E7EB;" required placeholder="doctor@medicare.com">
          </div>
          <div style="margin-bottom:15px;">
            <label style="display:block; margin-bottom:5px; font-size:13px; font-weight:500;">Password</label>
            <input type="password" id="add-doc-password" class="search-input" style="width:100%; border:1px solid #E5E7EB;" required placeholder="••••••••">
          </div>
          <button type="submit" class="submit-btn" style="width:100%; padding:12px;">Register Doctor</button>
          <div id="add-doc-msg" style="margin-top:10px; font-size:14px; text-align:center;"></div>
        </form>
      </div>
    `;
    document.body.appendChild(modal);
  }
  modal.classList.add('active');
};

window.closeAddDoctorModal = function() {
  const modal = document.getElementById('add-doctor-modal');
  if (modal) {
    modal.classList.remove('active');
    document.getElementById('add-doctor-form').reset();
    document.getElementById('add-doc-msg').innerText = '';
  }
};

window.handleAddDoctorSubmit = async function(e) {
  e.preventDefault();
  const fname = document.getElementById('add-doc-fname').value;
  const lname = document.getElementById('add-doc-lname').value;
  const email = document.getElementById('add-doc-email').value;
  const password = document.getElementById('add-doc-password').value;
  const msg = document.getElementById('add-doc-msg');
  
  msg.innerText = "Registering...";
  msg.style.color = "var(--gray-500)";
  
  try {
    const res = await fetch(`${window.MEDICARE_API_URL}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        first_name: fname,
        last_name: lname,
        email: email,
        password: password,
        role: 'doctor'
      })
    });
    
    const data = await res.json();
    if (res.ok) {
      msg.innerText = "Doctor registered successfully!";
      msg.style.color = "green";
      setTimeout(() => {
        closeAddDoctorModal();
        window.location.reload();
      }, 1500);
    } else {
      msg.innerText = data.detail || "Registration failed.";
      msg.style.color = "red";
    }
  } catch (err) {
    msg.innerText = "Connection error.";
    msg.style.color = "red";
  }
};

// In the dashboard init, check if we need to show the avatar & settings name fields
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
        
        // Prepopulate First & Last name settings fields
        const fnameInput = document.getElementById('admin-fname');
        const lnameInput = document.getElementById('admin-lname');
        if (fnameInput) fnameInput.value = me.first_name || '';
        if (lnameInput) lnameInput.value = me.last_name || '';
     }
  } catch(e) {}
}, 500);
