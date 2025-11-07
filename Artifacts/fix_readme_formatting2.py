#!/usr/bin/env python3
"""Fix markdown code block formatting in README.md - more aggressive approach"""

# Read the file as bytes first to see what we're dealing with
with open('README.md', 'rb') as f:
    raw_content = f.read()

# Decode with error handling
try:
    content = raw_content.decode('utf-8')
except:
    content = raw_content.decode('utf-8', errors='replace')

# More aggressive replacement - look for any pattern that starts with backslashes and ends with 'ash'
# Pattern: multiple backslashes, optional whitespace/control chars, 'ash'
content = re.sub(r'\\{2,}[\s\x08]*ash', '```bash', content)

# Replace any line that ends with multiple backslashes with ```
# This handles the closing marker
lines = content.split('\n')
new_lines = []
for line in lines:
    # Check if line ends with backslashes
    stripped = line.rstrip()
    if stripped.endswith('\\') and len(stripped) >= 2 and stripped.replace('\\', '').strip() == '':
        # Count backslashes
        backslash_count = len(stripped) - len(stripped.lstrip('\\'))
        if backslash_count >= 2:
            new_lines.append('```')
            continue
    new_lines.append(line)

content = '\n'.join(new_lines)

# Also fix the opening one more directly
content = content.replace('\\ash', '```bash')
content = content.replace('\\\ash', '```bash')
content = content.replace('\\\\ash', '```bash')
content = content.replace('\\\\\ash', '```bash')
content = content.replace('\\\\\\ash', '```bash')

# Write back
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed README.md formatting")

