import re

js_path = r"c:\Users\user\Desktop\doctor\frontend\js\admin.js"
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

# Fix grid avatar
old_grid = '`${window.MEDICARE_API_URL}${d.avatar_url}`'
new_grid = '`${d.avatar_url.startsWith("http") ? d.avatar_url : window.MEDICARE_API_URL + d.avatar_url}`'
js = js.replace(old_grid, new_grid)

# Fix openDoctorProfile avatar
old_dp = "av.src = window.MEDICARE_API_URL + d.avatar_url;"
new_dp = "av.src = d.avatar_url.startsWith('http') ? d.avatar_url : window.MEDICARE_API_URL + d.avatar_url;"
js = js.replace(old_dp, new_dp)

# Fix admin settings avatar preview in case it has the same issue
old_admin_preview = "preview.style.backgroundImage = `url(${window.MEDICARE_API_URL}${data.avatar_url})`;"
new_admin_preview = "preview.style.backgroundImage = `url(${data.avatar_url.startsWith('http') ? data.avatar_url : window.MEDICARE_API_URL + data.avatar_url})`;"
js = js.replace(old_admin_preview, new_admin_preview)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)

print("Fixed avatar URLs in admin.js")
