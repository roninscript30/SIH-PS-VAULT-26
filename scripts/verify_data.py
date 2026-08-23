#!/usr/bin/env python3
"""
SIH 2026 Data Verification Script
Re-fetches from the live website, independently parses every modal,
and cross-validates against the stored JSON to detect:
  - Missing problems
  - Extra/phantom problems
  - Truncated descriptions
  - Character encoding corruption
  - HTML artifacts in text fields
  - Field mismatches
  - ID sequence gaps
  - Duplicate entries
  - Data loss
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import os
import sys
import difflib

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}
URL = 'https://www.sih.gov.in/sih2026PS'
JSON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sih2026_problem_statements.json')

# ANSI colors for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

issues_found = []


def log_pass(msg):
    print(f"  {GREEN}✓ PASS{RESET}: {msg}")


def log_fail(msg):
    global issues_found
    issues_found.append(msg)
    print(f"  {RED}✗ FAIL{RESET}: {msg}")


def log_warn(msg):
    print(f"  {YELLOW}⚠ WARN{RESET}: {msg}")


def log_info(msg):
    print(f"  {CYAN}ℹ INFO{RESET}: {msg}")


def log_section(msg):
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  {msg}{RESET}")
    print(f"{BOLD}{'='*60}{RESET}")


def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.strip('×')
    return text


def independent_parse(html_content):
    """Completely independent parse of the HTML — no shared code with scraper.py"""
    soup = BeautifulSoup(html_content, 'html.parser')
    parsed = {}

    # Find ALL modals with ViewProblemStatement IDs
    modals = soup.find_all('div', id=re.compile(r'^ViewProblemStatement\d+'))

    for modal in modals:
        modal_id = modal.get('id', '')
        match = re.search(r'ViewProblemStatement(\d+)', modal_id)
        if not match:
            continue
        ps_id = match.group(1)
        if ps_id in parsed:
            continue

        entry = {'ps_id': ps_id}
        table = modal.find('table')
        if not table:
            continue

        for row in table.find_all('tr'):
            cells = row.find_all(['td', 'th'])
            if len(cells) < 2:
                continue
            key = clean_text(cells[0].get_text()).lower()
            val = clean_text(cells[1].get_text())

            if 'problem statement id' in key:
                entry['ps_id'] = val
            elif 'problem statement title' in key:
                entry['title'] = val
            elif key == 'description':
                entry['description'] = val
                # Also get raw HTML length for comparison
                entry['_desc_html_len'] = len(str(cells[1]))
            elif key == 'organization' or (key.startswith('organization') and 'type' not in key):
                entry['organization'] = val
            elif 'department' in key:
                entry['department'] = val
            elif key == 'category':
                entry['category'] = val
            elif key == 'theme':
                entry['theme'] = val
            elif 'youtube' in key:
                link = cells[1].find('a')
                entry['youtube_link'] = link.get('href', '') if link else val
            elif 'dataset' in key:
                link = cells[1].find('a')
                entry['dataset_link'] = link.get('href', '') if link else val
            elif 'contact' in key:
                entry['contact_info'] = val

        parsed[ps_id] = entry

    return parsed


def main():
    log_section("PHASE 1: RE-FETCH FROM LIVE WEBSITE")

    try:
        r = requests.get(URL, headers=HEADERS, timeout=60)
        r.raise_for_status()
        live_html = r.text
        log_pass(f"Live page fetched: {len(live_html):,} bytes, HTTP {r.status_code}")
    except Exception as e:
        log_fail(f"Cannot fetch live page: {e}")
        sys.exit(1)

    log_section("PHASE 2: INDEPENDENT PARSE OF LIVE HTML")

    live_data = independent_parse(live_html)
    log_info(f"Independently parsed {len(live_data)} problem statements from live HTML")

    log_section("PHASE 3: LOAD STORED JSON")

    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            stored = json.load(f)
        stored_problems = {ps['ps_id']: ps for ps in stored['problems']}
        log_pass(f"Loaded {len(stored_problems)} problems from JSON file")
    except Exception as e:
        log_fail(f"Cannot load JSON: {e}")
        sys.exit(1)

    log_section("PHASE 4: COUNT VERIFICATION")

    live_count = len(live_data)
    stored_count = len(stored_problems)
    if live_count == stored_count:
        log_pass(f"Count matches: {live_count} live == {stored_count} stored")
    else:
        log_fail(f"Count mismatch: {live_count} live vs {stored_count} stored")

    log_section("PHASE 5: MISSING & EXTRA PROBLEM IDS")

    live_ids = set(live_data.keys())
    stored_ids = set(stored_problems.keys())

    missing_from_json = live_ids - stored_ids
    extra_in_json = stored_ids - live_ids

    if not missing_from_json:
        log_pass("No problems missing from JSON (all live IDs accounted for)")
    else:
        for pid in sorted(missing_from_json):
            log_fail(f"PS {pid} exists on website but MISSING from JSON: \"{live_data[pid].get('title', '?')}\"")

    if not extra_in_json:
        log_pass("No phantom/extra problems in JSON (all JSON IDs exist on website)")
    else:
        for pid in sorted(extra_in_json):
            log_fail(f"PS {pid} in JSON but NOT on live website — phantom entry!")

    log_section("PHASE 6: ID SEQUENCE ANALYSIS")

    all_ids = sorted([int(x) for x in live_ids])
    expected_start = all_ids[0]
    expected_end = all_ids[-1]
    expected_count = expected_end - expected_start + 1
    actual_count = len(all_ids)

    log_info(f"ID range: {expected_start} → {expected_end}")
    log_info(f"Expected sequential count: {expected_count}, Actual: {actual_count}")

    if expected_count != actual_count:
        gaps = []
        for i in range(expected_start, expected_end + 1):
            if i not in [int(x) for x in live_ids]:
                gaps.append(i)
        if gaps:
            log_warn(f"ID gaps found (normal if SIH skips IDs): {gaps}")
    else:
        log_pass("IDs are sequential with no gaps")

    log_section("PHASE 7: FIELD-BY-FIELD COMPARISON (ALL PROBLEMS)")

    compare_fields = ['ps_id', 'title', 'description', 'organization', 'department', 'category', 'theme']
    field_mismatches = {f: [] for f in compare_fields}
    perfect_matches = 0

    common_ids = live_ids & stored_ids

    for pid in sorted(common_ids):
        live_ps = live_data[pid]
        stored_ps = stored_problems[pid]
        all_match = True

        for field in compare_fields:
            live_val = live_ps.get(field, '').strip()
            stored_val = stored_ps.get(field, '').strip()

            if live_val != stored_val:
                all_match = False
                field_mismatches[field].append(pid)

        if all_match:
            perfect_matches += 1

    log_info(f"Perfect matches (all fields identical): {perfect_matches}/{len(common_ids)}")

    for field in compare_fields:
        mismatches = field_mismatches[field]
        if not mismatches:
            log_pass(f"Field '{field}': All {len(common_ids)} entries match")
        else:
            log_fail(f"Field '{field}': {len(mismatches)} mismatches")
            for pid in mismatches[:5]:  # Show first 5
                live_val = live_data[pid].get(field, '')[:120]
                stored_val = stored_problems[pid].get(field, '')[:120]
                print(f"      PS {pid}:")
                print(f"        LIVE:   \"{live_val}\"")
                print(f"        STORED: \"{stored_val}\"")
            if len(mismatches) > 5:
                print(f"      ... and {len(mismatches) - 5} more")

    log_section("PHASE 8: DESCRIPTION INTEGRITY CHECK")

    truncation_suspects = []
    html_artifact_problems = []
    encoding_issues = []
    empty_descriptions = []

    html_patterns = [
        (re.compile(r'<(?:div|span|p|br|table|tr|td|th|a|img|ul|li|ol|h[1-6]|strong|em|b|i)\b', re.I), 'HTML tags'),
        (re.compile(r'&(?:amp|lt|gt|nbsp|quot|apos|#\d+|#x[0-9a-f]+);', re.I), 'HTML entities'),
    ]

    for pid in sorted(common_ids):
        desc = stored_problems[pid].get('description', '')

        # Check empty/very short
        if len(desc) < 30:
            empty_descriptions.append((pid, len(desc), desc[:80]))

        # Check for HTML artifacts
        for pattern, label in html_patterns:
            matches = pattern.findall(desc)
            if matches:
                html_artifact_problems.append((pid, label, matches[:3]))
                break

        # Check for encoding corruption (common indicators)
        encoding_markers = ['â€™', 'â€"', 'â€œ', 'â€', 'Â', '\ufffd', '\\u00']
        for marker in encoding_markers:
            if marker in desc:
                encoding_issues.append((pid, marker))
                break

        # Truncation check: compare live description length vs stored
        live_desc = live_data.get(pid, {}).get('description', '')
        if live_desc and desc:
            live_len = len(live_desc)
            stored_len = len(desc)
            if stored_len < live_len * 0.9:  # More than 10% shorter
                truncation_suspects.append((pid, live_len, stored_len))

    if not truncation_suspects:
        log_pass("No truncated descriptions detected (all within 10% of live length)")
    else:
        for pid, live_len, stored_len in truncation_suspects:
            log_fail(f"PS {pid}: Description possibly truncated — live={live_len} chars, stored={stored_len} chars ({stored_len*100//live_len}%)")

    if not html_artifact_problems:
        log_pass("No HTML tag artifacts found in descriptions")
    else:
        log_warn(f"{len(html_artifact_problems)} descriptions contain HTML artifacts")
        for pid, label, samples in html_artifact_problems[:5]:
            print(f"      PS {pid}: {label} → {samples}")

    if not encoding_issues:
        log_pass("No character encoding corruption detected")
    else:
        for pid, marker in encoding_issues:
            log_fail(f"PS {pid}: Encoding corruption detected ('{marker}')")

    if not empty_descriptions:
        log_pass("No empty/suspiciously short descriptions (all > 30 chars)")
    else:
        log_warn(f"{len(empty_descriptions)} descriptions are very short (< 30 chars)")
        for pid, length, preview in empty_descriptions:
            print(f"      PS {pid} ({length} chars): \"{preview}\"")

    log_section("PHASE 9: DATASET LINK VERIFICATION")

    # Compare dataset links
    live_datasets = {pid: ps.get('dataset_link', '').strip() for pid, ps in live_data.items() if ps.get('dataset_link', '').strip()}
    stored_datasets = {pid: ps.get('dataset_link', '').strip() for pid, ps in stored_problems.items() if ps.get('dataset_link', '').strip()}

    log_info(f"Live dataset links: {len(live_datasets)}, Stored dataset links: {len(stored_datasets)}")

    missing_datasets = set(live_datasets.keys()) - set(stored_datasets.keys())
    if not missing_datasets:
        log_pass("All dataset links preserved")
    else:
        for pid in missing_datasets:
            log_fail(f"PS {pid}: Dataset link lost — was: \"{live_datasets[pid][:100]}\"")

    log_section("PHASE 10: DUPLICATE DETECTION")

    # Check for duplicate titles (ignoring Student Innovation)
    title_map = {}
    for ps in stored['problems']:
        title = ps['title']
        if title == 'Student Innovation':
            continue
        if title in title_map:
            title_map[title].append(ps['ps_id'])
        else:
            title_map[title] = [ps['ps_id']]

    true_dupes = {t: ids for t, ids in title_map.items() if len(ids) > 1}
    if not true_dupes:
        log_pass("No duplicate titles found (excluding 'Student Innovation')")
    else:
        for title, ids in true_dupes.items():
            log_warn(f"Duplicate title \"{title[:80]}\" → IDs: {ids}")

    # Check Student Innovation count
    si_count = sum(1 for ps in stored['problems'] if ps['title'] == 'Student Innovation')
    log_info(f"'Student Innovation' entries: {si_count} (these are intentional open-ended themes)")

    log_section("PHASE 11: RANDOM DEEP SPOT-CHECK (5 SAMPLES)")

    import random
    random.seed(42)
    spot_ids = random.sample(list(common_ids), min(5, len(common_ids)))

    for pid in spot_ids:
        live_ps = live_data[pid]
        stored_ps = stored_problems[pid]

        print(f"\n  {CYAN}--- PS {pid}: \"{stored_ps.get('title', '?')[:60]}\" ---{RESET}")

        # Compare each field character by character
        all_ok = True
        for field in compare_fields:
            lv = live_ps.get(field, '')
            sv = stored_ps.get(field, '')
            if lv == sv:
                print(f"    {GREEN}✓{RESET} {field}: match ({len(sv)} chars)")
            else:
                all_ok = False
                # Show diff
                ratio = difflib.SequenceMatcher(None, lv, sv).ratio()
                print(f"    {RED}✗{RESET} {field}: MISMATCH (similarity: {ratio:.1%})")
                if len(lv) < 200:
                    print(f"      LIVE:   \"{lv}\"")
                    print(f"      STORED: \"{sv}\"")
                else:
                    # Show first divergence point
                    for i, (a, b) in enumerate(zip(lv, sv)):
                        if a != b:
                            print(f"      First diff at char {i}:")
                            print(f"        LIVE:   ...{lv[max(0,i-30):i+30]}...")
                            print(f"        STORED: ...{sv[max(0,i-30):i+30]}...")
                            break

        # Verify description contains key sections if present in live
        live_desc = live_ps.get('description', '')
        stored_desc = stored_ps.get('description', '')
        for section in ['Background:', 'Description:', 'Expected Solution:']:
            if section in live_desc and section not in stored_desc:
                print(f"    {RED}✗{RESET} Section '{section}' present in live but MISSING from stored!")
                all_ok = False

        if all_ok:
            print(f"    {GREEN}→ ALL FIELDS VERIFIED{RESET}")

    log_section("VERIFICATION SUMMARY")

    total_checks = len(common_ids) * len(compare_fields) + 10  # rough count
    if not issues_found:
        print(f"\n  {GREEN}{BOLD}✅ ALL CHECKS PASSED — DATA IS VERIFIED{RESET}")
        print(f"  {GREEN}   {len(stored_problems)} problems, all fields match live website{RESET}")
    else:
        print(f"\n  {RED}{BOLD}❌ {len(issues_found)} ISSUE(S) FOUND:{RESET}")
        for issue in issues_found:
            print(f"    {RED}• {issue}{RESET}")

    # Write verification report to file
    report = {
        'verification_timestamp': __import__('datetime').datetime.now().isoformat(),
        'source_url': URL,
        'live_problem_count': len(live_data),
        'stored_problem_count': len(stored_problems),
        'counts_match': len(live_data) == len(stored_problems),
        'missing_from_json': list(missing_from_json),
        'extra_in_json': list(extra_in_json),
        'id_range': f"{expected_start}-{expected_end}",
        'perfect_field_matches': perfect_matches,
        'field_mismatches': {f: len(v) for f, v in field_mismatches.items()},
        'truncation_suspects': len(truncation_suspects),
        'html_artifacts': len(html_artifact_problems),
        'encoding_issues': len(encoding_issues),
        'empty_descriptions': len(empty_descriptions),
        'duplicate_titles': len(true_dupes),
        'student_innovation_count': si_count,
        'total_issues': len(issues_found),
        'verdict': 'PASS' if not issues_found else 'FAIL',
        'issues': issues_found,
    }

    report_file = os.path.join(os.path.dirname(JSON_FILE), 'verification_report.json')
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    log_info(f"Verification report saved to {report_file}")


if __name__ == '__main__':
    main()
