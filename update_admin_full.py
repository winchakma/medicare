import re

file_path = r"c:\Users\user\Desktop\doctor\frontend\admin.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove Notifications and AI Reports from Sidebar
content = re.sub(r'<div class="nav-item" data-tab="notifications">.*?</div>\n', '', content)
content = re.sub(r'<div class="nav-item" data-tab="aireports">.*?</div>\n', '', content)

# Remove the badge from Appointments and add an ID
# Old: <div class="nav-item" data-tab="appointments"><span class="icon">📅</span> Appointments <span class="badge">8</span></div>
content = re.sub(r'<div class="nav-item" data-tab="appointments">.*?</div>', '<div class="nav-item" data-tab="appointments"><span class="icon">📅</span> Appointments <span class="badge" id="sidebar-appts-badge" style="display:none">0</span></div>', content)

# 2. Move bottom-row inside tab-dashboard
# We need to take the bottom-row and put it before the END tab-dashboard comment
bottom_row_pattern = r'<div class="bottom-row">.*?</div>\s*</div>\s*<!-- END tab-dashboard -->'
# Wait, currently the HTML structure is:
#     </div> <!-- END table-card -->
#     </div> <!-- END tab-dashboard -->
#     <!-- OTHER TABS -->
#     ...
#     </div> <!-- END content -->
# And bottom-row is inside tab-dashboard? Let me check where it is.
# Ah, I replaced `<div class="content">` with `<div class="content">\n    <!-- DASHBOARD TAB -->\n    <div id="tab-dashboard" class="admin-tab" style="display:block;">`
# And closed it at the end of content. So bottom-row IS inside tab-dashboard!
# Wait, if it is inside tab-dashboard, why did the user see it on the Doctors tab?
# Ah! Because the `bottom-row` was before the closing `</div>` of the `content` div.
# Yes, `</div> <!-- END tab-dashboard -->` was added by replacing `<script src="js/config.js">`.
# Wait, NO. My previous script added `</div> <!-- END tab-dashboard -->` right before the other tabs. Let me check the actual current file.
