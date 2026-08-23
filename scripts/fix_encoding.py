#!/usr/bin/env python3
"""
SIH 2026 — Fix encoding mojibake in scraped data.
The SIH website has CP1252→UTF-8 double-encoding on some descriptions.
Characters like â€™ → ', â€" → —, â€œ → ", â€ → ", Â → (non-breaking space)
"""

import json
import re
import os

JSON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sih2026_problem_statements.json')

# Known CP1252→UTF-8 mojibake patterns and their correct replacements
MOJIBAKE_MAP = {
    'â€™': '\u2019',  # '  (right single quotation mark)
    'â€˜': '\u2018',  # '  (left single quotation mark)
    'â€œ': '\u201C',  # "  (left double quotation mark)
    'â€\x9d': '\u201D',  # "  (right double quotation mark)
    'â€"': '\u2013',  # –  (en dash)
    'â€"': '\u2014',  # —  (em dash)
    'â€¢': '\u2022',  # •  (bullet)
    'â€¦': '\u2026',  # …  (ellipsis)
    'Â ': ' ',         # Non-breaking space artifact
    'Â·': '\u00B7',    # ·  (middle dot)
    'Ã©': 'é',
    'Ã¨': 'è',
    'Ã¼': 'ü',
    'Ã¶': 'ö',
    'Ã¤': 'ä',
    'Ã±': 'ñ',
}


def fix_mojibake(text):
    """Try to fix CP1252→UTF-8 double-encoding mojibake."""
    if not text:
        return text
    
    original = text
    
    # Method 1: Try the systematic cp1252→utf8 double-decode on segments
    # Find mojibake sequences and fix them individually
    def try_fix_segment(match):
        segment = match.group(0)
        try:
            fixed = segment.encode('cp1252').decode('utf-8')
            return fixed
        except (UnicodeDecodeError, UnicodeEncodeError):
            return segment
    
    # Pattern to find likely mojibake: â followed by €-range bytes
    # These are characteristic of UTF-8 multi-byte sequences misinterpreted as CP1252
    text = re.sub(r'â€[^\s]{0,2}', try_fix_segment, text)
    
    # Fix remaining known patterns
    for bad, good in MOJIBAKE_MAP.items():
        text = text.replace(bad, good)
    
    # Fix standalone Â before regular chars (artifact of Â+nbsp)
    text = re.sub(r'Â(?=\s)', '', text)
    
    # Normalize unicode
    # Convert curly quotes to straight for consistency (optional — preserving curly is also valid)
    # Actually, let's KEEP the proper Unicode chars and just clean up any remaining artifacts
    
    # Clean up any double spaces introduced by fixes
    text = re.sub(r'  +', ' ', text)
    
    return text


def main():
    print(f"Loading {JSON_FILE}...")
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixed_count = 0
    fix_details = []
    
    text_fields = ['title', 'description', 'organization', 'department', 'contact_info']
    
    for ps in data['problems']:
        ps_id = ps['ps_id']
        for field in text_fields:
            if field not in ps:
                continue
            original = ps[field]
            fixed = fix_mojibake(original)
            if fixed != original:
                fixed_count += 1
                # Show a sample of what changed
                # Find the first difference
                for i, (a, b) in enumerate(zip(original, fixed)):
                    if a != b:
                        ctx_start = max(0, i - 20)
                        ctx_end = min(len(original), i + 20)
                        fix_details.append(
                            f"  PS {ps_id}.{field}: ...{original[ctx_start:ctx_end]}... → ...{fixed[ctx_start:ctx_end]}..."
                        )
                        break
                ps[field] = fixed
    
    print(f"\nFixed {fixed_count} encoding issues across all problems")
    if fix_details:
        print("\nSample fixes:")
        for detail in fix_details[:15]:
            print(detail)
        if len(fix_details) > 15:
            print(f"  ... and {len(fix_details) - 15} more")
    
    # Save
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved fixed data to {JSON_FILE}")


if __name__ == '__main__':
    main()
