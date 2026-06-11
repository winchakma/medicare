import re

file_path = r"c:\Users\user\Desktop\doctor\frontend\admin.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace everything from <!-- BOTTOM ROW --> to <!-- END tab-dashboard -->
new_bottom_row = """    <!-- BOTTOM ROW -->
    <div class="bottom-row">
      <div class="bottom-card" id="top-doctors-list">
        <div style="font-size:14px;font-weight:600;margin-bottom:16px">Top Performing Doctors</div>
        <div style="padding:20px;text-align:center;">Loading...</div>
      </div>
      
      <div class="bottom-card" style="max-height: 400px; overflow-y: auto;">
        <div style="font-size:14px;font-weight:600;margin-bottom:16px">Recent Activity</div>
        <div id="admin-recent-activity">Loading activity...</div>
      </div>
    </div> <!-- END bottom-row -->
    </div> <!-- END tab-dashboard -->"""

content = re.sub(r'<!-- BOTTOM ROW -->.*?</div> <!-- END tab-dashboard -->', new_bottom_row, content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed DOM structure")
