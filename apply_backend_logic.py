import os

# 1. Create render.yaml
render_yaml = """services:
  - type: web
    name: medicare-api
    env: python
    buildCommand: "cd backend && pip install -r requirements.txt"
    startCommand: "cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
"""
with open('backend/render.yaml', 'w', encoding='utf-8') as f:
    f.write(render_yaml)

# 2. Create config.js
config_js = """/**
 * MEDICARE — GLOBAL CONFIGURATION
 */
(function() {
    if (window.MEDICARE_API_URL) return;

    const isLocal = window.location.hostname === 'localhost' || 
                    window.location.hostname === '127.0.0.1' || 
                    window.location.hostname.includes('192.168.');

    if (isLocal) {
        window.MEDICARE_API_URL = 'http://localhost:8000';
    } else {
        // PRODUCTION URL (Render)
        window.MEDICARE_API_URL = 'https://medicare-api-xyyl.onrender.com'; // User will deploy to Render
    }
    console.log(`MediCare API Target: ${window.MEDICARE_API_URL}`);
})();
"""
with open('frontend/js/config.js', 'w', encoding='utf-8') as f:
    f.write(config_js)

# 3. Update script.js to use MEDICARE_API_URL
with open('frontend/js/script.js', 'r', encoding='utf-8') as f:
    script_js = f.read()

script_js = script_js.replace("fetch('http://localhost:8000", "fetch(`${window.MEDICARE_API_URL || 'http://localhost:8000'}")
with open('frontend/js/script.js', 'w', encoding='utf-8') as f:
    f.write(script_js)

# 4. Inject config.js into all HTML files
html_files = [f for f in os.listdir('frontend') if f.endswith('.html')]
for f in html_files:
    path = os.path.join('frontend', f)
    with open(path, 'r', encoding='utf-8') as file:
        html = file.read()
    
    if 'src="js/config.js"' not in html:
        html = html.replace('<script src="js/script.js', '<script src="js/config.js"></script>\n<script src="js/script.js')
        with open(path, 'w', encoding='utf-8') as file:
            file.write(html)
