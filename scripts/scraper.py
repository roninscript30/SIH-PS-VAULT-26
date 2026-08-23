#!/usr/bin/env python3
"""
SIH 2026 Problem Statement Scraper
Extracts ALL problem statements from https://www.sih.gov.in/sih2026PS
Data is embedded in HTML modals (id=ViewProblemStatement{ID}) and tables (id=settings).
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import sys
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "sih2026_problem_statements.json")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

URL = 'https://www.sih.gov.in/sih2026PS'


def clean_text(text):
    """Clean extracted text - normalize whitespace, strip."""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove leading/trailing special chars
    text = text.strip('×')  # Modal close button artifacts
    return text


def extract_from_modals(soup):
    """Extract problem statements from modal divs."""
    problems = {}
    
    # Find all modals with ViewProblemStatement IDs
    modals = soup.find_all('div', id=re.compile(r'^ViewProblemStatement\d+'))
    print(f"Found {len(modals)} named modals (ViewProblemStatement*)")
    
    for modal in modals:
        modal_id = modal.get('id', '')
        ps_id_match = re.search(r'ViewProblemStatement(\d+)', modal_id)
        if not ps_id_match:
            continue
        
        ps_id = ps_id_match.group(1)
        
        if ps_id in problems:
            continue  # Skip duplicates
        
        ps = {
            'ps_id': ps_id,
            'source_modal_id': modal_id,
            'source_url': URL,
        }
        
        # Extract from modal body - look for table inside
        table = modal.find('table')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    key = clean_text(cells[0].get_text())
                    value = clean_text(cells[1].get_text())
                    
                    # Map to standardized field names
                    key_lower = key.lower().strip()
                    if 'problem statement id' in key_lower:
                        ps['ps_id'] = value
                    elif 'problem statement title' in key_lower or key_lower == 'title':
                        ps['title'] = value
                    elif 'description' in key_lower:
                        # Get raw HTML for description too (preserves formatting)
                        ps['description'] = value
                        ps['description_html'] = str(cells[1])
                    elif 'organization' in key_lower and 'type' not in key_lower:
                        ps['organization'] = value
                    elif 'organization type' in key_lower:
                        ps['organization_type'] = value
                    elif 'department' in key_lower:
                        ps['department'] = value
                    elif 'category' in key_lower:
                        ps['category'] = value
                    elif 'theme' in key_lower:
                        ps['theme'] = value
                    elif 'youtube' in key_lower:
                        # Extract actual URL if present
                        link = cells[1].find('a')
                        ps['youtube_link'] = link.get('href', '') if link else value
                    elif 'dataset' in key_lower:
                        link = cells[1].find('a')
                        ps['dataset_link'] = link.get('href', '') if link else value
                    elif 'contact' in key_lower:
                        ps['contact_info'] = value
                    else:
                        # Capture any unknown fields
                        if value:
                            safe_key = re.sub(r'[^a-z0-9_]', '_', key_lower).strip('_')
                            if safe_key:
                                ps[f'other_{safe_key}'] = value
        
        if ps.get('title') or ps.get('description'):
            problems[ps_id] = ps
    
    return problems


def extract_from_tables(soup):
    """Extract from the settings tables as a fallback/supplement."""
    problems = {}
    
    tables = soup.find_all('table', id='settings')
    print(f"Found {len(tables)} 'settings' tables")
    
    for table in tables:
        rows = table.find_all('tr')
        headers = []
        thead = table.find('thead')
        if thead:
            headers = [clean_text(th.get_text()) for th in thead.find_all('th')]
        
        tbody = table.find('tbody')
        if tbody:
            data_rows = tbody.find_all('tr')
            for row in data_rows:
                cells = row.find_all('td')
                if len(cells) >= len(headers):
                    ps = {'source_url': URL}
                    for idx, header in enumerate(headers):
                        value = clean_text(cells[idx].get_text()) if idx < len(cells) else ''
                        h_lower = header.lower()
                        
                        if 'problem statement id' in h_lower:
                            ps['ps_id'] = value
                        elif 'problem statement title' in h_lower:
                            ps['title'] = value
                        elif 'description' in h_lower:
                            ps['description'] = value
                            ps['description_html'] = str(cells[idx])
                        elif 'organization' in h_lower:
                            ps['organization'] = value
                        elif 'department' in h_lower:
                            ps['department'] = value
                        elif 'category' in h_lower:
                            ps['category'] = value
                        elif 'theme' in h_lower:
                            ps['theme'] = value
                        elif 'youtube' in h_lower:
                            link = cells[idx].find('a')
                            ps['youtube_link'] = link.get('href', '') if link else value
                        elif 'dataset' in h_lower:
                            link = cells[idx].find('a')
                            ps['dataset_link'] = link.get('href', '') if link else value
                        elif 'contact' in h_lower:
                            ps['contact_info'] = value
                    
                    ps_id = ps.get('ps_id', '')
                    if ps_id and (ps.get('title') or ps.get('description')):
                        if ps_id not in problems:
                            problems[ps_id] = ps
    
    return problems


def extract_card_titles(soup):
    """Extract problem titles from the card listing as a cross-reference."""
    titles = []
    # Look for the card-style links we saw in the scraped content
    # These are typically in an owl-carousel or card grid
    cards = soup.find_all('a', href=re.compile(r'sih2026PS'))
    seen = set()
    for card in cards:
        text = clean_text(card.get_text())
        if text and len(text) > 20 and text not in seen and 'Problem Statement Details' not in text:
            # Skip navigation links
            if text not in ['Problem Statements', 'Past Editions', 'About SIH', 'Guidelines',
                          'Home(current)', 'SIH Login', 'Contact us', 'Know Your SPOC',
                          'Know your SPOC', 'Login/Register', 'Project Implementation', 'FAQs']:
                seen.add(text)
                titles.append(text)
    return titles


def extract_all_modal_data_raw(soup):
    """More aggressive extraction - find ALL modals with problem data."""
    problems = {}
    
    # Find all divs with modal class
    all_modals = soup.find_all('div', class_='modal')
    print(f"Found {len(all_modals)} total modal divs")
    
    for modal in all_modals:
        modal_id = modal.get('id', '')
        
        # Skip non-PS modals
        if not modal_id.startswith('ViewProblemStatement'):
            # But also check if it contains problem statement data
            text = modal.get_text()
            if 'Problem Statement ID' not in text:
                continue
        
        # Extract PS ID from modal content
        table = modal.find('table')
        if not table:
            continue
            
        ps = {'source_url': URL, 'source_modal_id': modal_id}
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                key = clean_text(cells[0].get_text())
                value_cell = cells[1]
                value = clean_text(value_cell.get_text())
                
                key_lower = key.lower().strip()
                if 'problem statement id' in key_lower:
                    ps['ps_id'] = value
                elif 'problem statement title' in key_lower:
                    ps['title'] = value
                elif 'description' in key_lower:
                    ps['description'] = value
                    # Preserve HTML for rich description
                    ps['description_html'] = str(value_cell)
                elif 'organization' in key_lower and 'type' not in key_lower:
                    ps['organization'] = value
                elif 'organization type' in key_lower:
                    ps['organization_type'] = value
                elif 'department' in key_lower:
                    ps['department'] = value
                elif 'category' in key_lower:
                    ps['category'] = value
                elif 'theme' in key_lower:
                    ps['theme'] = value
                elif 'youtube' in key_lower:
                    link = value_cell.find('a')
                    ps['youtube_link'] = link.get('href', '') if link else value
                elif 'dataset' in key_lower:
                    link = value_cell.find('a')
                    ps['dataset_link'] = link.get('href', '') if link else value
                elif 'contact' in key_lower:
                    ps['contact_info'] = value
                else:
                    if value and key:
                        safe_key = re.sub(r'[^a-z0-9_]', '_', key_lower).strip('_')
                        if safe_key:
                            ps[f'other_{safe_key}'] = value
        
        ps_id = ps.get('ps_id', '')
        if ps_id and ps_id not in problems:
            problems[ps_id] = ps
    
    return problems


def merge_problem_data(modal_data, table_data, raw_modal_data):
    """Merge data from different extraction methods, preferring modal data."""
    all_ids = set(list(modal_data.keys()) + list(table_data.keys()) + list(raw_modal_data.keys()))
    merged = {}
    
    for ps_id in all_ids:
        ps = {}
        # Layer: table data first (least specific)
        if ps_id in table_data:
            ps.update(table_data[ps_id])
        # Layer: raw modal data
        if ps_id in raw_modal_data:
            ps.update({k: v for k, v in raw_modal_data[ps_id].items() if v})
        # Layer: named modal data (most specific)
        if ps_id in modal_data:
            ps.update({k: v for k, v in modal_data[ps_id].items() if v})
        
        merged[ps_id] = ps
    
    return merged


def validate_data(problems):
    """Validate extracted data and report issues."""
    issues = []
    valid = 0
    
    required_fields = ['ps_id', 'title', 'description', 'organization', 'category', 'theme']
    
    for ps_id, ps in problems.items():
        ps_issues = []
        for field in required_fields:
            if not ps.get(field):
                ps_issues.append(f"missing_{field}")
        
        if ps_issues:
            issues.append((ps_id, ps_issues))
        else:
            valid += 1
    
    return valid, issues


def main():
    print(f"Fetching SIH 2026 Problem Statements from {URL}...")
    
    try:
        r = requests.get(URL, headers=HEADERS, timeout=60)
        r.raise_for_status()
        print(f"Page fetched: {len(r.text)} bytes, status {r.status_code}")
    except Exception as e:
        print(f"Error fetching page: {e}")
        sys.exit(1)
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Save raw HTML for reference
    raw_path = os.path.join(OUTPUT_DIR, "sih2026_raw.html")
    with open(raw_path, 'w', encoding='utf-8') as f:
        f.write(r.text)
    print(f"Raw HTML saved to {raw_path}")
    
    # Extract from named modals
    print("\n--- Extracting from named modals ---")
    modal_data = extract_from_modals(soup)
    print(f"Extracted {len(modal_data)} problems from named modals")
    
    # Extract from tables
    print("\n--- Extracting from settings tables ---")
    table_data = extract_from_tables(soup)
    print(f"Extracted {len(table_data)} problems from tables")
    
    # Extract from ALL modals (aggressive)
    print("\n--- Extracting from all modals ---")
    raw_modal_data = extract_all_modal_data_raw(soup)
    print(f"Extracted {len(raw_modal_data)} problems from all modals")
    
    # Extract card titles for cross-reference
    print("\n--- Extracting card titles ---")
    card_titles = extract_card_titles(soup)
    print(f"Found {len(card_titles)} card titles on page")
    
    # Merge all data
    print("\n--- Merging data ---")
    problems = merge_problem_data(modal_data, table_data, raw_modal_data)
    print(f"Total unique problems after merge: {len(problems)}")
    
    # Validate
    print("\n--- Validation ---")
    valid, issues = validate_data(problems)
    print(f"Valid (all required fields): {valid}")
    print(f"With issues: {len(issues)}")
    if issues:
        for ps_id, ps_issues in issues[:10]:
            print(f"  PS {ps_id}: {', '.join(ps_issues)}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more")
    
    # Convert to list sorted by ID
    problems_list = sorted(problems.values(), key=lambda x: int(x.get('ps_id', '0')))
    
    # Remove description_html from JSON output (keep descriptions clean)
    for ps in problems_list:
        if 'description_html' in ps:
            del ps['description_html']
    
    # Summary stats
    categories = {}
    themes = {}
    organizations = {}
    for ps in problems_list:
        cat = ps.get('category', 'Unknown')
        theme = ps.get('theme', 'Unknown')
        org = ps.get('organization', 'Unknown')
        categories[cat] = categories.get(cat, 0) + 1
        themes[theme] = themes.get(theme, 0) + 1
        organizations[org] = organizations.get(org, 0) + 1
    
    output = {
        'metadata': {
            'source': URL,
            'scraped_at': __import__('datetime').datetime.now().isoformat(),
            'total_problems': len(problems_list),
            'categories': categories,
            'themes': themes,
            'organizations': organizations,
            'card_titles_found': len(card_titles),
            'validation': {
                'valid': valid,
                'with_issues': len(issues),
                'issues_detail': {ps_id: ps_issues for ps_id, ps_issues in issues}
            }
        },
        'problems': problems_list
    }
    
    # Save
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n=== DONE ===")
    print(f"Saved {len(problems_list)} problem statements to {OUTPUT_FILE}")
    print(f"\nCategories: {json.dumps(categories, indent=2)}")
    print(f"\nThemes ({len(themes)} unique):")
    for t, count in sorted(themes.items(), key=lambda x: -x[1]):
        print(f"  {t}: {count}")
    print(f"\nOrganizations ({len(organizations)} unique):")
    for o, count in sorted(organizations.items(), key=lambda x: -x[1])[:20]:
        print(f"  {o}: {count}")


if __name__ == '__main__':
    main()
