import re

html_path = r"c:\Users\user\Desktop\doctor\frontend\admin.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

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

# Find where to insert it. Let's insert it before <div id="auth-modal"
if "tab-doctor-profile" not in html:
    html = html.replace('  </div>\n</div>\n\n<script', doctor_profile_html + '\n  </div>\n</div>\n\n<script')

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated admin.html")

main_path = r"c:\Users\user\Desktop\doctor\backend\main.py"
with open(main_path, "r", encoding="utf-8") as f:
    main_code = f.read()

if "StaticFiles" not in main_code:
    main_code = main_code.replace("from fastapi import FastAPI", "from fastapi import FastAPI\nfrom fastapi.staticfiles import StaticFiles\nimport os")
    static_mount = """
os.makedirs("uploads/avatars", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
"""
    main_code = main_code.replace('app = FastAPI(title="MediCare API")', 'app = FastAPI(title="MediCare API")\n' + static_mount)
    with open(main_path, "w", encoding="utf-8") as f:
        f.write(main_code)
    print("Updated main.py")
