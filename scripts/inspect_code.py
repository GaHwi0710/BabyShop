import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('backend/src/modules/reports/reports.route.js', 'r', encoding='utf-8') as f:
    text = f.read()

routes = re.findall(r'router\.get\(\s*["\']([^"\']+)["\']', text)
print("Total router.get in reports.route.js:", len(routes))
for i, r in enumerate(routes):
    print(f"{i+1}: {r}")
