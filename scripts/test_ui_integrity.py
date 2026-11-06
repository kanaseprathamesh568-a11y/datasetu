import re
import sys

with open("datasetu/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Find all getElementById calls
id_matches = re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", html)
print(f"Total getElementById calls: {len(id_matches)}")

# Find all existing ids in html
existing_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))
print(f"Total defined IDs in HTML: {len(existing_ids)}")

missing_ids = set()
for elem_id in id_matches:
    # Some IDs are dynamically computed or template literals
    if "${" in elem_id:
        continue
    if elem_id not in existing_ids:
        missing_ids.add(elem_id)

print(f"Missing IDs referenced in JS: {len(missing_ids)}")
for m in sorted(missing_ids):
    print("  - MISSING ID:", m)

# 2. Find all onclick/onchange/onsubmit functions
events = re.findall(r'on(?:click|change|submit)=["\']([a-zA-Z0-9_]+)\(', html)
print(f"\nTotal inline event handlers: {len(events)}")
unique_events = set(events)

# Find all defined functions in <script> tags
defined_funcs = set(re.findall(r"function\s+([a-zA-Z0-9_]+)\s*\(", html))
# Also arrow functions / const func = ...
arrow_funcs = set(re.findall(r"(?:const|let|var)\s+([a-zA-Z0-9_]+)\s*=\s*(?:async\s*)?\(", html))
all_funcs = defined_funcs | arrow_funcs
print(f"Total defined functions in scripts: {len(all_funcs)}")

missing_funcs = set()
for func in unique_events:
    if func not in all_funcs:
        missing_funcs.add(func)

print(f"Missing functions referenced in event handlers: {len(missing_funcs)}")
for func in sorted(missing_funcs):
    print("  - MISSING FUNC:", func)

# 3. Find all fetch() endpoints
fetches = re.findall(r"fetch\((?:`([^`]+)`|'([^']+)'|\"([^\"]+)\")", html)
print(f"\nTotal fetch calls: {len(fetches)}")
endpoints = set()
for f1, f2, f3 in fetches:
    ep = f1 or f2 or f3
    endpoints.add(ep)
for ep in sorted(endpoints):
    print("  - FETCH ENDPOINT:", ep)

