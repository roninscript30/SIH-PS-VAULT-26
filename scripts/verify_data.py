#!/usr/bin/env python3
"""
SIH 2026 Comprehensive Data & Vault Verification Suite
Validates dataset count, ID continuity, source snapshot/live integrity,
JSON ↔ Markdown consistency, relative link integrity, and taxonomy pages.
"""

import os
import sys
import json
import re
import glob
import requests
import difflib
from bs4 import BeautifulSoup

# Add script directory to sys.path to allow execution from any directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from vault_config import (VAULT_ROOT, JSON_FILE, RAW_HTML_FILE,
                          VERIFICATION_REPORT_FILE, SOURCE_URL, DIRS)

# ANSI colors for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

issues_found = []
warnings_found = []

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}


def log_pass(msg):
    print(f"  {GREEN}✓ PASS{RESET}: {msg}")


def log_fail(msg):
    global issues_found
    issues_found.append(msg)
    print(f"  {RED}✗ FAIL{RESET}: {msg}")


def log_warn(msg):
    global warnings_found
    warnings_found.append(msg)
    print(f"  {YELLOW}⚠ WARN{RESET}: {msg}")


def log_info(msg):
    print(f"  {CYAN}ℹ INFO{RESET}: {msg}")


def log_section(msg):
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  {msg}{RESET}")
    print(f"{BOLD}{'='*60}{RESET}")


def try_fix_segment(match):
    segment = match.group(0)
    try:
        return segment.encode('cp1252').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        return segment


def normalize_text(text):
    """Normalize text for consistent comparison across raw source and cleaned dataset.
    Repairs CP1252 double-encoding mojibake and normalizes whitespace.
    """
    if not text:
        return ""

    mojibake_map = {
        'â€™': '’', 'â€˜': '‘', 'â€œ': '“', 'â€\x9d': '”', 'â€ ': '”',
        'â€”': '—', 'â€“': '–', 'â€•': '—', 'â€¢': '•',
        'â€¦': '…', 'Â ': ' ', 'Â·': '·', 'Â°': '°',
        'Âµ': 'µ', 'Ã—': '×', 'Ã±': 'ñ', 'Ã©': 'é',
        'Ã¨': 'è', 'Ã¼': 'ü', 'Ã¶': 'ö', 'Ã¤': 'ä'
    }
    for bad, good in mojibake_map.items():
        text = text.replace(bad, good)

    text = re.sub(r'â€[^\s]{0,2}', try_fix_segment, text)
    text = re.sub(r'Â(?![°µ×])', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.strip('×')


def independent_parse_html(html_content):
    """Parse modal problem statement data from raw HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    parsed = {}

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
            key = cells[0].get_text().strip().lower()
            val = cells[1].get_text().strip()

            if 'problem statement id' in key:
                entry['ps_id'] = val
            elif 'problem statement title' in key:
                entry['title'] = val
            elif key == 'description':
                entry['description'] = val
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
    log_section("PHASE 1: LOAD SOURCE SNAPSHOT & LIVE DATA")

    source_html = None
    try:
        r = requests.get(SOURCE_URL, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            source_html = r.text
            log_pass(f"Live portal fetched successfully ({len(source_html):,} bytes)")
    except Exception:
        log_info("Live portal unavailable or offline; using local raw snapshot")

    if not source_html:
        if os.path.exists(RAW_HTML_FILE):
            with open(RAW_HTML_FILE, 'r', encoding='utf-8') as f:
                source_html = f.read()
            log_pass(f"Loaded local source snapshot: {RAW_HTML_FILE} ({len(source_html):,} bytes)")
        else:
            log_fail("Neither live portal nor local raw HTML snapshot is available")
            sys.exit(1)

    source_data = independent_parse_html(source_html)
    log_info(f"Independently parsed {len(source_data)} problem statements from source HTML")

    log_section("PHASE 2: LOAD & VALIDATE STORED JSON DATASET")

    if not os.path.exists(JSON_FILE):
        log_fail(f"JSON dataset file missing: {JSON_FILE}")
        sys.exit(1)

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        stored_data = json.load(f)

    stored_problems = {ps['ps_id']: ps for ps in stored_data.get('problems', [])}
    log_pass(f"Loaded {len(stored_problems)} problem statements from JSON dataset")

    # Count verification
    expected_count = len(source_data) if source_data else len(stored_problems)
    if len(stored_problems) == expected_count:
        log_pass(f"Expected dataset count verified ({len(stored_problems)} Problem Statements)")
    else:
        log_fail(f"Dataset count discrepancy: found {len(stored_problems)}, expected {expected_count}")

    # Sequence & Range
    int_ids = sorted([int(pid) for pid in stored_problems.keys()])
    expected_end_id = 26000 + len(stored_problems)
    if int_ids[0] == 26001 and int_ids[-1] == expected_end_id and len(int_ids) == len(stored_problems):
        log_pass(f"IDs are strictly continuous from 26001 to {expected_end_id} (no gaps, no duplicates)")
    else:
        log_fail(f"ID sequence anomaly: range {int_ids[0]} to {int_ids[-1]}, total {len(int_ids)}")

    log_section("PHASE 3: RAW HTML ↔ STORED JSON FIELD COMPARISON")

    compare_fields = ['ps_id', 'title', 'description', 'organization', 'department', 'category', 'theme']
    mismatch_counts = {f: 0 for f in compare_fields}

    for pid, source_ps in source_data.items():
        if pid not in stored_problems:
            log_fail(f"PS {pid} present in source HTML but missing from JSON dataset!")
            continue
        stored_ps = stored_problems[pid]

        for field in compare_fields:
            src_val = normalize_text(source_ps.get(field, ''))
            std_val = normalize_text(stored_ps.get(field, ''))

            if src_val != std_val:
                mismatch_counts[field] += 1
                log_fail(f"PS {pid} field '{field}' mismatch between source and dataset")

    if sum(mismatch_counts.values()) == 0:
        log_pass("All fields match source HTML snapshot 100% after text normalization")
    else:
        log_fail(f"Field mismatches found: {mismatch_counts}")

    log_section("PHASE 4: MARKDOWN VAULT ↔ JSON CONSISTENCY")

    ps_md_dir = os.path.join(VAULT_ROOT, DIRS['ps'])
    md_files = glob.glob(os.path.join(ps_md_dir, 'PS-*.md'))
    log_info(f"Found {len(md_files)} Markdown problem statement files in {DIRS['ps']}/")

    if len(md_files) == len(stored_problems):
        log_pass(f"Markdown problem statement file count matches JSON ({len(md_files)} files)")
    else:
        log_fail(f"Markdown file count discrepancy: {len(md_files)} files vs {len(stored_problems)} expected")

    md_mismatches = 0
    for pid, ps in stored_problems.items():
        expected_md = os.path.join(ps_md_dir, f"PS-{pid}.md")
        if not os.path.exists(expected_md):
            log_fail(f"Markdown file missing for PS-{pid}: {expected_md}")
            md_mismatches += 1
            continue

        with open(expected_md, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check frontmatter ps_id
        fm_id_match = re.search(r'ps_id:\s*["\']?(\d+)["\']?', content)
        if not fm_id_match or fm_id_match.group(1) != pid:
            log_fail(f"PS-{pid}.md frontmatter ID mismatch or missing!")
            md_mismatches += 1

        # Check title in frontmatter
        fm_title_match = re.search(r'title:\s*["\'](.*?)["\']\n', content)
        if fm_title_match:
            clean_fm_title = fm_title_match.group(1).replace("'", '"')
            clean_json_title = ps['title'].replace("'", '"')
            if clean_fm_title[:40] != clean_json_title[:40]:
                log_fail(f"PS-{pid}.md frontmatter title does not match JSON title")
                md_mismatches += 1

    if md_mismatches == 0:
        log_pass(f"All {len(stored_problems)} Markdown PS files match JSON dataset IDs and titles")

    log_section("PHASE 5: INTERNAL RELATIVE LINK INTEGRITY")

    all_md = glob.glob(os.path.join(VAULT_ROOT, '**/*.md'), recursive=True)
    broken_links = []
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    for filepath in all_md:
        file_dir = os.path.dirname(filepath)
        rel_file = os.path.relpath(filepath, VAULT_ROOT)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        for match in link_pattern.finditer(content):
            link_target = match.group(2)

            if link_target.startswith(('http://', 'https://', '#', 'mailto:')):
                continue

            target_path = link_target.split('#')[0]
            if not target_path:
                continue

            abs_target = os.path.abspath(os.path.join(file_dir, target_path))
            if not os.path.exists(abs_target):
                broken_links.append((rel_file, link_target))

    if not broken_links:
        log_pass(f"Validated relative links across {len(all_md)} Markdown files (0 broken links)")
    else:
        for src, tgt in broken_links[:10]:
            log_fail(f"Broken relative link in {src} ➔ {tgt}")

    log_section("PHASE 6: STALE & ORPHANED ARTIFACT CHECK")

    expected_generated_files = set()
    for pid in stored_problems.keys():
        expected_generated_files.add(os.path.abspath(os.path.join(ps_md_dir, f"PS-{pid}.md")))

    orphan_files = []
    for fname in os.listdir(ps_md_dir):
        if fname.endswith('.md'):
            fpath = os.path.abspath(os.path.join(ps_md_dir, fname))
            if fpath not in expected_generated_files:
                orphan_files.append(fname)

    if not orphan_files:
        log_pass("Zero orphaned or stale problem statement files in vault")
    else:
        for ofile in orphan_files:
            log_fail(f"Orphaned file found in PS directory: {ofile}")

    log_section("VERIFICATION SUMMARY")

    verdict = 'PASS' if not issues_found else 'FAIL'
    if issues_found:
        print(f"\n  {RED}{BOLD}❌ VERDICT: FAIL ({len(issues_found)} issues found){RESET}")
        for issue in issues_found:
            print(f"    • {RED}{issue}{RESET}")
    elif warnings_found:
        print(f"\n  {YELLOW}{BOLD}⚠️ VERDICT: PASS WITH WARNINGS ({len(warnings_found)} warnings){RESET}")
    else:
        print(f"\n  {GREEN}{BOLD}✅ VERDICT: PASS — ALL CHECKS PASSED PERFECTLY{RESET}")
        print(f"  {GREEN}   {len(stored_problems)} Problem Statements verified, 0 broken links, 0 mismatches{RESET}")

    # Generate verification report JSON artifact
    report = {
        'verification_timestamp': __import__('datetime').datetime.now().isoformat(),
        'source_url': SOURCE_URL,
        'dataset_file': os.path.relpath(JSON_FILE, VAULT_ROOT),
        'total_problems': len(stored_problems),
        'id_range': f"{int_ids[0]}-{int_ids[-1]}",
        'field_mismatches': mismatch_counts,
        'markdown_ps_count': len(md_files),
        'broken_links_count': len(broken_links),
        'orphan_files_count': len(orphan_files),
        'issues_count': len(issues_found),
        'warnings_count': len(warnings_found),
        'verdict': verdict,
        'issues': issues_found,
    }

    with open(VERIFICATION_REPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    log_info(f"Verification report saved to {os.path.relpath(VERIFICATION_REPORT_FILE, VAULT_ROOT)}")

    if verdict == 'FAIL':
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
