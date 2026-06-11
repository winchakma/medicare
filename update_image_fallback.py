import re

js_path = r"c:\Users\user\Desktop\doctor\frontend\js\admin.js"
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

# Fix the grid rendering fallback
old_img = "`${window.MEDICARE_API_URL}${d.avatar_url}`"
# Wait, it's:
# ${d.avatar_url ? `<img src="${window.MEDICARE_API_URL}${d.avatar_url}" style="width:50px; height:50px; border-radius:50%; object-fit:cover;">` : `<div class="mini-avatar" style="width:50px; height:50px; font-size:16px; background:#185FA5;">${d.name.substring(4, 6).toUpperCase()}</div>`}

old_grid_avatar = '                  ${d.avatar_url ? `<img src="${window.MEDICARE_API_URL}${d.avatar_url}" style="width:50px; height:50px; border-radius:50%; object-fit:cover;">` : `<div class="mini-avatar" style="width:50px; height:50px; font-size:16px; background:#185FA5;">${d.name.substring(4, 6).toUpperCase()}</div>`}'
new_grid_avatar = '                  ${d.avatar_url ? `<img src="${window.MEDICARE_API_URL}${d.avatar_url}" onerror="this.onerror=null; this.style.display=\'none\'; this.nextElementSibling.style.display=\'flex\';" style="width:50px; height:50px; border-radius:50%; object-fit:cover;"><div class="mini-avatar" style="width:50px; height:50px; font-size:16px; background:#185FA5; display:none;">${d.name.substring(4, 6).toUpperCase()}</div>` : `<div class="mini-avatar" style="width:50px; height:50px; font-size:16px; background:#185FA5;">${d.name.substring(4, 6).toUpperCase()}</div>`}'

js = js.replace(old_grid_avatar, new_grid_avatar)

# Fix openDoctorProfile fallback
old_dp_logic = """  const av = document.getElementById('dp-avatar');
  const ini = document.getElementById('dp-initials');
  if (d.avatar_url) {
    av.src = window.MEDICARE_API_URL + d.avatar_url;
    av.style.display = 'block';
    ini.style.display = 'none';
  } else {
    av.style.display = 'none';
    ini.style.display = 'flex';
    ini.innerText = d.name.substring(4, 6).toUpperCase();
  }"""

new_dp_logic = """  const av = document.getElementById('dp-avatar');
  const ini = document.getElementById('dp-initials');
  
  av.onerror = function() {
    av.style.display = 'none';
    ini.style.display = 'flex';
    ini.innerText = d.name.substring(4, 6).toUpperCase();
  };

  if (d.avatar_url) {
    av.src = window.MEDICARE_API_URL + d.avatar_url;
    av.style.display = 'block';
    ini.style.display = 'none';
  } else {
    av.style.display = 'none';
    ini.style.display = 'flex';
    ini.innerText = d.name.substring(4, 6).toUpperCase();
  }"""

js = js.replace(old_dp_logic, new_dp_logic)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)

print("Updated admin.js with image fallbacks")
