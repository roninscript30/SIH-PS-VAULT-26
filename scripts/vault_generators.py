"""Generators for individual problem statement files and concept catalog pages."""
import os
from collections import Counter
from vault_config import DIRS, sanitize_filename, SOURCE_URL, classify_org_type, rel_link


def generate_ps_file(ps, vault_root):
    """Generate a clean, structured problem statement markdown file."""
    ps_id = ps['ps_id']
    title = ps['title']
    org = ps['organization']
    dept = ps['department']
    cat = ps['category']
    theme = ps['theme']
    techs = ps.get('_technologies', [])
    domains = ps.get('_domains', [])
    sections = ps.get('_sections', {})
    similar = ps.get('_similar', [])
    org_type = ps.get('_org_type', 'Unknown')
    dataset_link = ps.get('dataset_link', '').strip()
    youtube_link = ps.get('youtube_link', '').strip()
    has_dataset = bool(dataset_link)

    org_fname = sanitize_filename(org)
    theme_fname = sanitize_filename(theme)
    sub_ps = DIRS['ps']

    # YAML Frontmatter
    tech_yaml = '\n'.join(f'  - "{t}"' for t in techs) if techs else '  - "General"'
    domain_yaml = '\n'.join(f'  - "{d}"' for d in domains) if domains else '  - "General"'
    alias_parts = [f'PS {ps_id}', f'SIH {ps_id}']
    if len(title) > 25:
        alias_parts.append(title[:50].rsplit(' ', 1)[0])
    aliases_yaml = '\n'.join(f'  - "{a}"' for a in alias_parts)

    fm = f"""---
# Official SIH Metadata
ps_id: "{ps_id}"
title: "{title.replace('"', "'")}"
organization: "{org.replace('"', "'")}"
department: "{dept.replace('"', "'")}"
category: "{cat}"
theme: "{theme}"
source_url: "{SOURCE_URL}"

# Derived Metadata (Vault Enriched)
organization_type: "{org_type}"
technologies:
{tech_yaml}
domains:
{domain_yaml}
has_dataset: {str(has_dataset).lower()}
aliases:
{aliases_yaml}
tags:
  - sih2026
  - {cat.lower()}
  - {theme_fname.lower()}
---
"""

    org_l = rel_link(org, sub_ps, DIRS['orgs'], org_fname)
    theme_l = rel_link(theme, sub_ps, DIRS['themes'], theme_fname)

    body = f"# PS {ps_id} — {title}\n\n"
    body += f"> [!info] Quick Reference\n"
    body += f"> **Organization**: {org_l}\n"
    if dept and dept != org:
        body += f"> **Department**: {dept}\n"
    body += f"> **Theme**: {theme_l} | **Category**: {cat} | **Type**: {org_type}\n"
    body += f"> **Official Links**: [SIH Portal]({SOURCE_URL})"
    if dataset_link and dataset_link.startswith(('http://', 'https://')):
        body += f" · [Dataset/Reference]({dataset_link})"
    if youtube_link and youtube_link.startswith(('http://', 'https://')):
        body += f" · [Official Video]({youtube_link})"
    body += "\n"
    if dataset_link and not dataset_link.startswith(('http://', 'https://')):
        body += f"> **Dataset Reference Note**: {dataset_link}\n"
    body += "\n\n"

    # Classifications
    body += "### 🔧 Key Classifications\n\n"
    if techs:
        tech_links = [rel_link(t, sub_ps, DIRS['tech'], t) for t in techs]
        body += "**Technologies**: " + " · ".join(tech_links) + "\n\n"
    if domains:
        domain_links = [rel_link(d, sub_ps, DIRS['domains'], d) for d in domains]
        body += "**Domains**: " + " · ".join(domain_links) + "\n\n"

    body += "---\n\n## 📋 Official Problem Statement\n\n"

    bg = sections.get('background', '')
    desc = sections.get('description', '')
    es = sections.get('expected_solution', '')

    if bg:
        body += "### Background\n\n" + bg + "\n\n"
    if desc:
        body += "### Problem Description\n\n" + desc + "\n\n"
    if es:
        body += "### Expected Solution & Deliverables\n\n" + es + "\n\n"

    if cat == 'Hardware':
        body += "> [!note] Hardware Category\n> This problem statement requires a physical hardware prototype submission.\n\n"

    # Related Problems
    if similar:
        body += "---\n\n## 🔗 Related Problem Statements\n\n"
        for s in similar:
            reasons = ', '.join(s['reasons'])
            ps_l = rel_link(f"PS-{s['ps_id']}", sub_ps, sub_ps, f"PS-{s['ps_id']}")
            body += f"- {ps_l} — {s['title'][:75]} *({reasons})*\n"
        body += "\n"

    filepath = os.path.join(vault_root, DIRS['ps'], f"PS-{ps_id}.md")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fm + body)
    return filepath


def generate_theme_page(theme, problems, vault_root):
    """Generate a theme catalog page."""
    theme_ps = [p for p in problems if p['theme'] == theme]
    sw = sum(1 for p in theme_ps if p['category'] == 'Software')
    hw = sum(1 for p in theme_ps if p['category'] == 'Hardware')
    fname = sanitize_filename(theme)
    sub = DIRS['themes']

    idx_link = rel_link("← Theme Catalog Index", sub, sub, "theme_index.md")

    content = f"""---
type: theme
theme: "{theme}"
problem_count: {len(theme_ps)}
software_count: {sw}
hardware_count: {hw}
tags:
  - sih2026
  - theme
---
# 🏷️ {theme}

{idx_link}

> **{len(theme_ps)} Problem Statements** ({sw} Software, {hw} Hardware)

## 📋 Problem Statements in {theme}

| PS ID | Title | Organization | Category |
|-------|-------|-------------|----------|
"""
    for ps in sorted(theme_ps, key=lambda x: int(x['ps_id'])):
        pid = ps['ps_id']
        t = ps['title'][:70]
        org = ps['organization'][:35]
        cat = ps['category']
        ps_l = rel_link(f"PS-{pid}", sub, DIRS['ps'], f"PS-{pid}")
        org_l = rel_link(org, sub, DIRS['orgs'], sanitize_filename(ps['organization']))
        content += f"| {ps_l} | {t} | {org_l} | {cat} |\n"

    all_techs = []
    for p in theme_ps:
        all_techs.extend(p.get('_technologies', []))
    tech_counts = Counter(all_techs).most_common(8)
    if tech_counts:
        content += "\n## 🔧 Top Technologies\n\n"
        for tech, count in tech_counts:
            tl = rel_link(tech, sub, DIRS['tech'], tech)
            content += f"- {tl} — {count} problems\n"

    org_counts = Counter(p['organization'] for p in theme_ps).most_common()
    content += "\n## 🏢 Participating Organizations\n\n"
    for org, count in org_counts:
        ol = rel_link(org, sub, DIRS['orgs'], sanitize_filename(org))
        content += f"- {ol} — {count} problems\n"

    filepath = os.path.join(vault_root, DIRS['themes'], f"{fname}.md")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath


def generate_org_page(org, problems, vault_root):
    """Generate an organization catalog page."""
    org_ps = [p for p in problems if p['organization'] == org]
    fname = sanitize_filename(org)
    org_type = classify_org_type(org)
    depts = set(p['department'] for p in org_ps if p['department'] != org and p['department'])
    sw = sum(1 for p in org_ps if p['category'] == 'Software')
    hw = sum(1 for p in org_ps if p['category'] == 'Hardware')
    sub = DIRS['orgs']

    idx_link = rel_link("← Organization Catalog Index", sub, sub, "organization_index.md")

    content = f"""---
type: organization
organization: "{org.replace('"', "'")}"
organization_type: "{org_type}"
problem_count: {len(org_ps)}
tags:
  - sih2026
  - organization
  - {org_type.lower()}
---
# 🏢 {org}

{idx_link}

> **Type**: {org_type} | **{len(org_ps)} Problem Statements** ({sw} Software, {hw} Hardware)

"""
    if depts:
        content += "**Departments**: " + ', '.join(depts) + "\n\n"

    content += """## 📋 Problem Statements

| PS ID | Title | Category | Theme |
|-------|-------|----------|-------|
"""
    for ps in sorted(org_ps, key=lambda x: int(x['ps_id'])):
        pid = ps['ps_id']
        t = ps['title'][:65]
        cat = ps['category']
        theme = ps['theme']
        ps_l = rel_link(f"PS-{pid}", sub, DIRS['ps'], f"PS-{pid}")
        theme_l = rel_link(theme, sub, DIRS['themes'], sanitize_filename(theme))
        content += f"| {ps_l} | {t} | {cat} | {theme_l} |\n"

    themes = Counter(p['theme'] for p in org_ps).most_common()
    content += "\n## 🏷️ Theme Breakdown\n\n"
    for theme, count in themes:
        tl = rel_link(theme, sub, DIRS['themes'], sanitize_filename(theme))
        content += f"- {tl} — {count} problems\n"

    filepath = os.path.join(vault_root, DIRS['orgs'], f"{fname}.md")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath


def generate_tech_page(tech, problems, vault_root):
    """Generate a technology concept catalog page."""
    tech_ps = [p for p in problems if tech in p.get('_technologies', [])]
    fname = tech
    sub = DIRS['tech']

    idx_link = rel_link("← Technology Catalog Index", sub, sub, "technology_index.md")

    content = f"""---
type: technology
technology: "{tech}"
problem_count: {len(tech_ps)}
tags:
  - sih2026
  - technology
---
# 🔧 {tech.replace('-', ' ')}

{idx_link}

> **{len(tech_ps)} Problem Statements** leverage this technology

## 📋 Problem Statements

| PS ID | Title | Organization | Category | Theme |
|-------|-------|-------------|----------|-------|
"""
    for ps in sorted(tech_ps, key=lambda x: int(x['ps_id'])):
        pid = ps['ps_id']
        t = ps['title'][:60]
        org = ps['organization'][:28]
        cat = ps['category']
        theme = ps['theme'][:22]
        ps_l = rel_link(f"PS-{pid}", sub, DIRS['ps'], f"PS-{pid}")
        org_l = rel_link(org, sub, DIRS['orgs'], sanitize_filename(ps['organization']))
        theme_l = rel_link(theme, sub, DIRS['themes'], sanitize_filename(ps['theme']))
        content += f"| {ps_l} | {t} | {org_l} | {cat} | {theme_l} |\n"

    cotech = Counter()
    for p in tech_ps:
        for t in p.get('_technologies', []):
            if t != tech:
                cotech[t] += 1
    if cotech:
        content += "\n## 🔗 Frequently Co-occurring Technologies\n\n"
        for t, c in cotech.most_common(8):
            tl = rel_link(t, sub, sub, t)
            content += f"- {tl} — {c} shared problems\n"

    filepath = os.path.join(vault_root, DIRS['tech'], f"{fname}.md")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath


def generate_domain_page(domain, problems, vault_root):
    """Generate a domain classification catalog page."""
    domain_ps = [p for p in problems if domain in p.get('_domains', [])]
    fname = domain
    sub = DIRS['domains']

    idx_link = rel_link("← Domain Catalog Index", sub, sub, "domain_index.md")

    content = f"""---
type: domain
domain: "{domain}"
problem_count: {len(domain_ps)}
tags:
  - sih2026
  - domain
---
# 📊 {domain.replace('-', ' ')}

{idx_link}

> **{len(domain_ps)} Problem Statements** fall in this domain

## 📋 Problem Statements

| PS ID | Title | Organization | Category | Theme |
|-------|-------|-------------|----------|-------|
"""
    for ps in sorted(domain_ps, key=lambda x: int(x['ps_id'])):
        pid = ps['ps_id']
        t = ps['title'][:55]
        org = ps['organization'][:25]
        cat = ps['category']
        theme = ps['theme'][:20]
        ps_l = rel_link(f"PS-{pid}", sub, DIRS['ps'], f"PS-{pid}")
        org_l = rel_link(org, sub, DIRS['orgs'], sanitize_filename(ps['organization']))
        theme_l = rel_link(theme, sub, DIRS['themes'], sanitize_filename(ps['theme']))
        content += f"| {ps_l} | {t} | {org_l} | {cat} | {theme_l} |\n"

    filepath = os.path.join(vault_root, DIRS['domains'], f"{fname}.md")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath
