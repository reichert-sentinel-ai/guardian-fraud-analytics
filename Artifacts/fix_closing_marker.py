#!/usr/bin/env python3
"""Fix closing code block markers"""

# Read the file
with open('README.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix lines that have escaped backslashes and backticks
new_lines = []
for i, line in enumerate(lines):
    # Check if line contains escaped backslashes and backticks like '\\`'
    if '\\`' in line and line.strip().replace('\\', '').replace('`', '').strip() == '':
        # This is a closing marker, replace with ```
        new_lines.append('```\n')
    else:
        new_lines.append(line)

# Write back
with open('README.md', 'w', encoding='utf-8', newline='\n') as f:
    f.writelines(new_lines)

print("Fixed closing markers")

