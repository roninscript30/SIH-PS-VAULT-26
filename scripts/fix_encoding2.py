#!/usr/bin/env python3
"""Fix remaining encoding artifacts: degree symbols, micro symbols, multiplication signs, remaining dashes."""
import json
import re

JSON_FILE = '/home/marudhu/REPOS/SIH-PS-VAULT-26/sih2026_problem_statements.json'

with open(JSON_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

fixes = 0
for ps in data['problems']:
    for field in ['description', 'title', 'organization', 'department']:
        if field not in ps:
            continue
        original = ps[field]
        text = original

        # Fix: Â° → ° (degree symbol)
        text = text.replace('Â°', '°')
        # Fix: Âµ → µ (micro symbol)  
        text = text.replace('Âµ', 'µ')
        # Fix: Ã— → × (multiplication)
        text = text.replace('\u00c3\u2014', '\u00d7')
        text = text.replace('Ã\u2014', '×')
        text = text.replace('Ã—', '×')
        # Fix remaining mojibake dashes
        # â€" can be em-dash or en-dash
        # Try cp1252 decode for any remaining â€ sequences
        def fix_remaining(match):
            seg = match.group(0)
            try:
                return seg.encode('cp1252').decode('utf-8')
            except:
                return seg
        
        text = re.sub(r'â€.', fix_remaining, text)
        
        # Clean standalone Â (non-breaking space artifacts, but NOT before ° or µ)
        # Only remove Â that isn't part of a valid sequence
        text = re.sub(r'Â(?![°µ×])', '', text)

        if text != original:
            fixes += 1
            ps[field] = text

print(f'Applied {fixes} additional fixes')

with open(JSON_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Saved.')

# Final verification
markers = ['Â°', 'Âµ', 'Ã—', 'â€']
remaining = 0
for ps in data['problems']:
    desc = ps.get('description', '')
    for marker in markers:
        if marker in desc:
            remaining += 1
            # Show context
            idx = desc.index(marker)
            print(f'  PS {ps["ps_id"]}: ...{desc[max(0,idx-20):idx+20]}...')
            break

print(f'\nRemaining encoding artifacts: {remaining}')
