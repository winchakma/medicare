import re

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Fix grid gaps by using auto-fit instead of auto-fill
css = css.replace('repeat(auto-fill, minmax(130px, 1fr))', 'repeat(auto-fit, minmax(130px, 1fr))')
css = css.replace('repeat(auto-fill, minmax(260px, 1fr))', 'repeat(auto-fit, minmax(260px, 1fr))')

# 2. Limit maximum width on large screens by calculating dynamic padding
# This preserves full-width backgrounds (like hero, navy sections, nav) while centering content.
css = css.replace('padding: 60px 5%;', 'padding: 60px max(5%, calc((100vw - 1200px) / 2));')
css = css.replace('padding: 80px 5%;', 'padding: 80px max(5%, calc((100vw - 1200px) / 2));')
css = css.replace('padding: 90px 5% 0;', 'padding: 90px max(5%, calc((100vw - 1200px) / 2)) 0;')
css = css.replace('padding: 0 5%;', 'padding: 0 max(5%, calc((100vw - 1200px) / 2));')
css = css.replace('margin: 0 5% 60px;', 'margin: 0 max(5%, calc((100vw - 1200px) / 2)) 60px;')
css = css.replace('padding: 32px 5%;', 'padding: 32px max(5%, calc((100vw - 1200px) / 2));')
css = css.replace('padding: 16px 5%;', 'padding: 16px max(5%, calc((100vw - 1200px) / 2));')
css = css.replace('padding: 28px 5%;', 'padding: 28px max(5%, calc((100vw - 1200px) / 2));')

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("CSS updated successfully.")
