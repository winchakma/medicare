import re

file_path = r"c:\Users\user\Desktop\doctor\frontend\admin.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update the nav items to have data-tab attributes
# The sidebar nav is around lines 19-32
nav_html = """  <div class="sidebar-nav">
    <div class="nav-section-label">Main</div>
    <div class="nav-item active" data-tab="dashboard"><span class="icon">📊</span> Dashboard</div>
    <div class="nav-item" data-tab="appointments"><span class="icon">📅</span> Appointments <span class="badge">8</span></div>
    <div class="nav-item" data-tab="doctors"><span class="icon">👨‍⚕️</span> Doctors</div>
    <div class="nav-item" data-tab="patients"><span class="icon">🧑‍🤝‍🧑</span> Patients</div>
    <div class="nav-section-label">Finance</div>
    <div class="nav-item" data-tab="revenue"><span class="icon">💰</span> Revenue</div>
    <div class="nav-item" data-tab="invoices"><span class="icon">🧾</span> Invoices</div>
    <div class="nav-section-label">System</div>
    <div class="nav-item" data-tab="settings"><span class="icon">⚙️</span> Settings</div>
    <div class="nav-item" data-tab="notifications"><span class="icon">🔔</span> Notifications <span class="badge">3</span></div>
    <div class="nav-item" data-tab="aireports"><span class="icon">🤖</span> AI Reports</div>
  </div>"""

# Replace the old sidebar nav
old_nav_regex = r'<div class="sidebar-nav">.*?</div>\s*<div class="sidebar-user">'
content = re.sub(old_nav_regex, nav_html + '\n  <div class="sidebar-user">', content, flags=re.DOTALL)

# 2. Wrap the current content in a tab
content = content.replace('<div class="content">', '<div class="content">\n    <!-- DASHBOARD TAB -->\n    <div id="tab-dashboard" class="admin-tab" style="display:block;">')

# 3. Add closing div for tab-dashboard and add other tabs before </div><!-- MAIN --> or similar
# The end of the content div is before the <script> tags.
# Let's find the end of the bottom-row.
# Actually, we can just replace `<script src="js/config.js">` with the new tabs closing the content.

other_tabs = """
    </div> <!-- END tab-dashboard -->

    <!-- OTHER TABS -->
    <div id="tab-appointments" class="admin-tab" style="display:none; padding: 40px; text-align: center;">
      <div style="font-size:48px; margin-bottom: 20px;">📅</div>
      <h2>Appointments Management</h2>
      <p style="color:var(--gray-500); margin-top: 10px;">Full appointment scheduling and management module coming soon.</p>
    </div>
    
    <div id="tab-doctors" class="admin-tab" style="display:none; padding: 40px; text-align: center;">
      <div style="font-size:48px; margin-bottom: 20px;">👨‍⚕️</div>
      <h2>Doctors Directory</h2>
      <p style="color:var(--gray-500); margin-top: 10px;">Doctor onboarding, verification, and profile management module coming soon.</p>
    </div>
    
    <div id="tab-patients" class="admin-tab" style="display:none; padding: 40px; text-align: center;">
      <div style="font-size:48px; margin-bottom: 20px;">🧑‍🤝‍🧑</div>
      <h2>Patient Records</h2>
      <p style="color:var(--gray-500); margin-top: 10px;">Electronic health records (EHR) and patient management coming soon.</p>
    </div>
    
    <div id="tab-revenue" class="admin-tab" style="display:none; padding: 40px; text-align: center;">
      <div style="font-size:48px; margin-bottom: 20px;">💰</div>
      <h2>Revenue Analytics</h2>
      <p style="color:var(--gray-500); margin-top: 10px;">Detailed financial breakdowns and payout management coming soon.</p>
    </div>

    <div id="tab-invoices" class="admin-tab" style="display:none; padding: 40px; text-align: center;">
      <div style="font-size:48px; margin-bottom: 20px;">🧾</div>
      <h2>Invoices & Billing</h2>
      <p style="color:var(--gray-500); margin-top: 10px;">Automated invoice generation and billing history coming soon.</p>
    </div>
    
    <div id="tab-settings" class="admin-tab" style="display:none; padding: 40px; text-align: center;">
      <div style="font-size:48px; margin-bottom: 20px;">⚙️</div>
      <h2>System Settings</h2>
      <p style="color:var(--gray-500); margin-top: 10px;">Platform configuration, localization, and API integrations coming soon.</p>
    </div>
    
    <div id="tab-notifications" class="admin-tab" style="display:none; padding: 40px; text-align: center;">
      <div style="font-size:48px; margin-bottom: 20px;">🔔</div>
      <h2>Notification Center</h2>
      <p style="color:var(--gray-500); margin-top: 10px;">SMS, Email, and Push notification templates and history coming soon.</p>
    </div>
    
    <div id="tab-aireports" class="admin-tab" style="display:none; padding: 40px; text-align: center;">
      <div style="font-size:48px; margin-bottom: 20px;">🤖</div>
      <h2>AI Health Reports</h2>
      <p style="color:var(--gray-500); margin-top: 10px;">Predictive analytics and AI-generated platform health reports coming soon.</p>
    </div>

  </div> <!-- END content -->
</div> <!-- END main -->
"""

# Replace the end of the main div
content = re.sub(r'    </div>\n  </div>\n</div>\n\n<script src="js/config.js">', other_tabs + '\n<script src="js/config.js">', content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)


# 4. Update admin.js to handle tab clicks
js_path = r"c:\Users\user\Desktop\doctor\frontend\js\admin.js"
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

tab_script = """
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
"""

if "Tab Switching Logic" not in js_content:
    js_content = js_content.replace('// Set today\'s date in top bar', tab_script + '\n  // Set today\'s date in top bar')
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_content)

print("Updated tabs.")
