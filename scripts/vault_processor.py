"""Data processing: extraction, normalization, section parsing, similarity detection."""
import re
from vault_config import TECH_KEYWORDS, DOMAIN_KEYWORDS, classify_org_type


def extract_technologies(ps):
    """Extract normalized technology tags from title + description."""
    text = ps.get('title', '') + ' ' + ps.get('description', '')
    techs = []
    for tech, patterns in TECH_KEYWORDS.items():
        for pat in patterns:
            if re.search(pat, text, re.IGNORECASE):
                techs.append(tech)
                break
    return sorted(set(techs))


def extract_domains(ps):
    """Extract domain classifications from title + description."""
    text = ps.get('title', '') + ' ' + ps.get('description', '')
    domains = []
    for domain, patterns in DOMAIN_KEYWORDS.items():
        for pat in patterns:
            if re.search(pat, text, re.IGNORECASE):
                domains.append(domain)
                break
    return sorted(set(domains))


def clean_text(text):
    """Clean raw text artifacts and format lists into clean markdown."""
    if not text:
        return ''
    text = text.replace('•', '\n- ')
    text = re.sub(r'(\s+|^)([a-z0-9])\.\s+', r'\n- ', text)
    lines = []
    for line in text.split('\n'):
        l = line.strip()
        if l:
            if l.startswith('-'):
                l = '- ' + l[1:].strip()
            lines.append(l)
    
    result = []
    for l in lines:
        if l.startswith('-'):
            result.append(l)
        else:
            if result and not result[-1].startswith('-'):
                result.append('')
            result.append(l)
    
    res = '\n'.join(result).strip()
    res = re.sub(r'\.\s*\.+$', '.', res)
    return res


def parse_description_sections(desc):
    """Split description into Background, Description, Expected Solution."""
    sections = {'background': '', 'description': '', 'expected_solution': '', 'full': desc}
    bg_match = re.search(r'Background:\s*(.*?)(?=Description:|Expected Solution:|$)', desc, re.DOTALL | re.IGNORECASE)
    desc_match = re.search(r'(?<!Problem Statement )Description:\s*(.*?)(?=Expected Solution:|$)', desc, re.DOTALL | re.IGNORECASE)
    es_match = re.search(r'Expected Solution:\s*(.*?)$', desc, re.DOTALL | re.IGNORECASE)
    
    if bg_match:
        sections['background'] = clean_text(bg_match.group(1).strip())
    if desc_match:
        sections['description'] = clean_text(desc_match.group(1).strip())
    if es_match:
        sections['expected_solution'] = clean_text(es_match.group(1).strip())
    if not any([sections['background'], sections['description'], sections['expected_solution']]):
        sections['description'] = clean_text(desc)
    return sections


def detect_similarities(all_problems):
    """Find related/similar problems based on tech overlap, org, theme, domain overlap."""
    similarities = {}
    for i, ps1 in enumerate(all_problems):
        ps_id = ps1['ps_id']
        related = []
        for j, ps2 in enumerate(all_problems):
            if i == j:
                continue
            score = 0
            reasons = []
            if ps1['organization'] == ps2['organization'] and ps1['organization'] != 'AICTE':
                score += 2
                reasons.append('same organization')
            if ps1['theme'] == ps2['theme']:
                score += 1
                reasons.append('same theme')
            t1 = set(ps1.get('_technologies', []))
            t2 = set(ps2.get('_technologies', []))
            overlap = t1 & t2
            if len(overlap) >= 3:
                score += 2
                reasons.append(f'tech overlap ({len(overlap)})')
            elif len(overlap) >= 2:
                score += 1
                reasons.append(f'tech overlap ({len(overlap)})')
            d1 = set(ps1.get('_domains', []))
            d2 = set(ps2.get('_domains', []))
            d_overlap = d1 & d2
            if len(d_overlap) >= 2:
                score += 1
                reasons.append('domain overlap')

            if score >= 2:
                related.append({'ps_id': ps2['ps_id'], 'title': ps2['title'], 'score': score, 'reasons': reasons})

        related.sort(key=lambda x: -x['score'])
        similarities[ps_id] = related[:5]
    return similarities


def process_all(problems):
    """Main processing pipeline: enrich all problems with extracted metadata."""
    for ps in problems:
        ps['_technologies'] = extract_technologies(ps)
        ps['_domains'] = extract_domains(ps)
        ps['_sections'] = parse_description_sections(ps.get('description', ''))
        ps['_org_type'] = classify_org_type(ps.get('organization', ''))
    
    similarities = detect_similarities(problems)
    for ps in problems:
        ps['_similar'] = similarities.get(ps['ps_id'], [])
    return problems
