import re

file_path = r"c:\Users\user\Desktop\doctor\frontend\admin.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace total bookings value
content = content.replace('<div class="stat-card-value">1,284</div>', '<div class="stat-card-value" id="stat-total-bookings">...</div>')
# Replace total revenue
content = content.replace('<div class="stat-card-value">$98,400</div>', '<div class="stat-card-value" id="stat-total-revenue">...</div>')
# Replace active doctors
content = content.replace('<div class="stat-card-value">147</div>', '<div class="stat-card-value" id="stat-active-doctors">...</div>')
# Replace total patients
content = content.replace('<div class="stat-card-value">8,932</div>', '<div class="stat-card-value" id="stat-total-patients">...</div>')

# Table body
tbody_original = r"<tbody>.*?</tbody>"
tbody_new = '<tbody id="admin-appointments-list"><tr><td colspan="8" style="text-align:center;padding:20px;">Loading appointments...</td></tr></tbody>'
content = re.sub(tbody_original, tbody_new, content, flags=re.DOTALL)

# Pagination row
pag_original = r'<div class="pagination-row">.*?</div>\s*</div>'
pag_new = '<div class="pagination-row" id="admin-appointments-pagination"></div>\n    </div>'
content = re.sub(pag_original, pag_new, content, flags=re.DOTALL)

# Top Performing Doctors
bottom_original = r'<div class="bottom-card">.*?<div style="font-size:14px;font-weight:600;margin-bottom:16px">Top Performing Doctors</div>.*?</div>\s*<div class="bottom-card">'
bottom_new = '<div class="bottom-card" id="top-doctors-list">\n        <div style="font-size:14px;font-weight:600;margin-bottom:16px">Top Performing Doctors</div>\n        <div style="padding:20px;text-align:center;">Loading...</div>\n      </div>\n      <div class="bottom-card">'
content = re.sub(bottom_original, bottom_new, content, flags=re.DOTALL)

# Add admin.js script at the end
if '<script src="js/admin.js"></script>' not in content:
    content = content.replace('</body>', '<script src="js/admin.js"></script>\n</body>')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated admin.html")
