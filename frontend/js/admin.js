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
    // 1. Fetch dashboard stats
    const statsRes = await fetch(`${window.MEDICARE_API_URL}/api/admin/dashboard-stats`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!statsRes.ok) throw new Error("Failed to load stats");
    const stats = await statsRes.json();

    document.getElementById('stat-total-bookings').innerText = stats.total_bookings.toLocaleString();
    document.getElementById('stat-total-revenue').innerText = '$' + stats.total_revenue.toLocaleString();
    document.getElementById('stat-active-doctors').innerText = stats.active_doctors.toLocaleString();
    document.getElementById('stat-total-patients').innerText = stats.total_patients.toLocaleString();

    // 2. Fetch appointments
    const apptsRes = await fetch(`${window.MEDICARE_API_URL}/api/admin/appointments`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!apptsRes.ok) throw new Error("Failed to load appointments");
    const appts = await apptsRes.json();

    const tbody = document.getElementById('admin-appointments-list');
    tbody.innerHTML = '';
    appts.forEach(a => {
      let statusClass = 'status-pending';
      if (a.status === 'confirmed') statusClass = 'status-confirmed';
      if (a.status === 'cancelled') statusClass = 'status-cancelled';

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td style="font-weight:500;color:var(--navy)">${a.booking_id}</td>
        <td>${a.patient_name}</td>
        <td><div class="doc-cell"><div class="mini-avatar" style="background:#0D9B76">${a.doctor_initials}</div>${a.doctor_name}</div></td>
        <td>${a.specialty}</td>
        <td>${a.date} &middot; ${a.time_slot}</td>
        <td style="font-weight:500">$${a.fee}</td>
        <td><span class="status-badge ${statusClass}">${a.status}</span></td>
        <td><div class="action-btns"><button class="act-btn">View</button></div></td>
      `;
      tbody.appendChild(tr);
    });

    if (appts.length === 0) {
      tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:20px;">No recent appointments found.</td></tr>';
    }

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

    // 3. Fetch top doctors
    const docsRes = await fetch(`${window.MEDICARE_API_URL}/api/admin/top-doctors`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (docsRes.ok) {
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

        if (topDocs.length === 0) {
          topDocsContainer.innerHTML += '<div style="padding:10px;text-align:center;color:#666;">No bookings yet.</div>';
        }
      }
    }

  } catch (err) {
    console.error(err);
  }
});
