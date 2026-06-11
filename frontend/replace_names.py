import os

replacements = {
    "Dr. Sarah Ahmed": "Dr. Sarah Miller",
    "Dr. Rafiq Khan": "Dr. Richard Kane",
    "Dr. Nadia Islam": "Dr. Natalie Irons",
    "Dr. Mahbub Hossain": "Dr. Matthew Hayes",
    "Dhaka": "New York",
    "Chittagong": "Los Angeles",
    "Sylhet": "Chicago",
    "৳800": "$80",
    "৳1,200": "$120",
    "৳600": "$60",
    "৳1,500": "$150",
    "৳": "$"
}

html_files = [f for f in os.listdir('.') if f.endswith('.html')]
for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Replacements complete.")
