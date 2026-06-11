import re

js_path = r"c:\Users\user\Desktop\doctor\frontend\js\admin.js"
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

def replace_sequential_with_parallel(code):
    # We will find the entire DOMContentLoaded async arrow function
    # and we will define a bunch of async functions inside and then call them all at once!
    
    # Let's just wrap each try...catch block in an IIFE (Immediately Invoked Function Expression)
    # so they run concurrently!
    # For example, replace `try {` with `(async () => { try {`
    # and the matching `} catch(e) {}` with `} catch(e) {} })();`
    
    blocks = [
        r"// 1\. Fetch dashboard stats",
        r"// 2\. Fetch appointments",
        r"// 3\. Fetch top doctors",
        r"// 4\. Fetch all appointments",
        r"// 5\. Fetch Doctors",
        r"// 6\. Fetch Patients",
        r"// 7\. Fetch Recent Activity"
    ]
    
    new_js = js
    
    # Block 1
    new_js = new_js.replace(
        "try {\n    // 1. Fetch dashboard stats",
        "(async () => {\n  try {\n    // 1. Fetch dashboard stats"
    )
    # Block 2
    new_js = new_js.replace(
        "// 2. Fetch appointments",
        "} catch(e) {} })();\n\n(async () => {\n  try {\n    // 2. Fetch appointments"
    )
    # Block 3
    new_js = new_js.replace(
        "// 3. Fetch top doctors",
        "} catch(e) {} })();\n\n(async () => {\n  try {\n    // 3. Fetch top doctors"
    )
    # Block 4
    new_js = new_js.replace(
        "// 4. Fetch all appointments",
        "} catch(e) {} })();\n\n(async () => {\n  try {\n    // 4. Fetch all appointments"
    )
    # Block 5
    new_js = new_js.replace(
        "// 5. Fetch Doctors",
        "} catch(e) {} })();\n\n(async () => {\n  try {\n    // 5. Fetch Doctors"
    )
    # Block 6
    new_js = new_js.replace(
        "// 6. Fetch Patients",
        "} catch(e) {} })();\n\n(async () => {\n  try {\n    // 6. Fetch Patients"
    )
    # Block 7
    new_js = new_js.replace(
        "// 7. Fetch Recent Activity",
        "} catch(e) {} })();\n\n(async () => {\n  try {\n    // 7. Fetch Recent Activity"
    )
    
    # End of block 7
    new_js = new_js.replace(
        "    } catch(e) {}\n\n    // Handle settings form",
        "    } catch(e) {} })();\n\n    // Handle settings form"
    )

    return new_js

new_js = replace_sequential_with_parallel(js)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(new_js)

print("Refactored admin.js to load concurrently!")
