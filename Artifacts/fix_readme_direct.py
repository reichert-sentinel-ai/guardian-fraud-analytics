#!/usr/bin/env python3
"""Fix markdown code block formatting - direct byte-level replacement"""

# Read as bytes
with open('README.md', 'rb') as f:
    content_bytes = f.read()

# Decode
content = content_bytes.decode('utf-8', errors='replace')

# Direct replacements for the problematic patterns
# Replace any line that starts with backslashes followed by 'ash'
lines = content.split('\n')
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Check if this line matches the pattern for opening code block
    stripped = line.strip()
    
    # Pattern: starts with backslashes and contains 'ash'
    if stripped.startswith('\\') and 'ash' in stripped.lower():
        new_lines.append('```bash')
    # Pattern: line with just backslashes (closing marker)
    elif stripped.replace('\\', '').strip() == '' and len(stripped) >= 2:
        new_lines.append('```')
    else:
        new_lines.append(line)
    i += 1

content = '\n'.join(new_lines)

# Write back
with open('README.md', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Fixed README.md formatting")

