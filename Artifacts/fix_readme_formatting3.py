#!/usr/bin/env python3
"""Fix markdown code block formatting in README.md - remove extra backslashes"""

import re

# Read the file
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove backslashes before backticks in code block markers
# Pattern: backslashes followed by three backticks
content = re.sub(r'\\+```', '```', content)

# Also fix any remaining issues with backslash-ash patterns
content = re.sub(r'\\+ash', '```bash', content)

# Fix closing markers - backslashes before closing backticks
content = re.sub(r'\\+```', '```', content)

# Write back
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed README.md formatting - removed extra backslashes")

