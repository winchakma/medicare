import re

file_path = r"c:\Users\user\Desktop\doctor\frontend\admin.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix the extra closing divs that prematurely close tab-dashboard
content = content.replace('      </div>\n    </div>\n\n    <!-- BOTTOM ROW -->', '    <!-- BOTTOM ROW -->')

# Remove Notifications and AI Reports from the nav
content = re.sub(r'<div class="nav-item" data-tab="notifications">.*?</div>\n\s*', '', content)
content = re.sub(r'<div class="nav-item" data-tab="aireports">.*?</div>\n\s*', '', content)

# Remove them from the tabs
content = re.sub(r'<div id="tab-notifications".*?</div>', '', content, flags=re.DOTALL)
content = re.sub(r'<div id="tab-aireports".*?</div>', '', content, flags=re.DOTALL)

# Add ID to appointments badge
content = re.sub(r'<div class="nav-item" data-tab="appointments">.*?</div>', '<div class="nav-item" data-tab="appointments"><span class="icon">📅</span> Appointments <span class="badge" id="sidebar-appts-badge" style="display:none">0</span></div>', content)

# Make sure bottom-row is inside tab-dashboard properly
# We need to make sure the end of tab-dashboard is right after bottom-row.
# It currently is at: `    </div> <!-- END tab-dashboard -->`
# Let's verify that later.

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed HTML")
