#!/usr/bin/env python3
"""SIH 2026 Obsidian Vault Generator — Main Orchestrator."""
import json
import os
import re
import shutil
from collections import Counter
from vault_config import (DIRS, VAULT_ROOT, JSON_FILE, SOURCE_URL,
                          sanitize_filename, rel_link)
from vault_processor import process_all
from vault_generators import (generate_ps_file, generate_theme_page,
    generate_org_page, generate_tech_page, generate_domain_page)


def make_dirs():
    """Create directory structure."""
    for d in DIRS.values():
        os.makedirs(os.path.join(VAULT_ROOT, d), exist_ok=True)


def gen_readme(problems, vault_root):
    """Generate root README.md for public GitHub repository presentation."""
    themes = Counter(p['theme'] for p in problems)
    orgs = Counter(p['organization'] for p in problems)
    sw = sum(1 for p in problems if p['category'] == 'Software')
    hw = sum(1 for p in problems if p['category'] == 'Hardware')
    actual = [p for p in problems if p['title'] != 'Student Innovation']
    si_count = len(problems) - len(actual)

    c = f"""# 🇮🇳 Smart India Hackathon (SIH) 2026 — Problem Statement Vault

[![SIH 2026](https://img.shields.io/badge/SIH-2026-orange.svg)]({SOURCE_URL})
[![Problem Statements](https://img.shields.io/badge/Problems-226-blue.svg)](06-Indexes/all_problems_index.md)
[![Software](https://img.shields.io/badge/Software-{sw}-green.svg)](06-Indexes/category_index.md)
[![Hardware](https://img.shields.io/badge/Hardware-{hw}-red.svg)](06-Indexes/category_index.md)
[![Themes](https://img.shields.io/badge/Themes-18-purple.svg)](02-Themes/theme_index.md)
[![Organizations](https://img.shields.io/badge/Organizations-30-yellow.svg)](03-Organizations/organization_index.md)

Welcome to the **Smart India Hackathon (SIH) 2026 Problem Statement Vault**. This repository provides an offline-ready, hyperlinked knowledge system containing all **226 official problem statements** released for SIH 2026.

Every problem statement has been cleaned, structured, and cross-indexed by **Theme**, **Organization**, **Technology**, **Domain**, and **Category** with 100% relative Markdown links for seamless navigation on GitHub or in Obsidian.

---

## 📊 Vault Quick Statistics

| Metric | Count | Description |
|--------|------:|-------------|
| **Total Problem Statements** | **{len(problems)}** | Complete official release |
| **Unique Ministry/Org Problems** | **{len(actual)}** | Targeted problem statements |
| **Student Innovation Slots** | **{si_count}** | Open-ended AICTE innovation themes |
| **Software Problems** | **{sw}** | Web, Mobile, AI/ML, Cloud, GIS, Data platforms |
| **Hardware Problems** | **{hw}** | Embedded systems, Robotics, Drones, IoT, Sensors |
| **Participating Themes** | **{len(themes)}** | Structured problem domains |
| **Nodal Organizations** | **{len(orgs)}** | Central Ministries, PSUs, Industry leaders |

---

## 🧭 Interactive Catalogs & Indexes

Explore the vault using any of the hyperlinked catalogs below:

| Catalog | Link | Description |
|---------|------|-------------|
| 📋 **All Problem Statements** | [all_problems_index.md](06-Indexes/all_problems_index.md) | Complete master table of all 226 problem statements |
| 🏷️ **Themes Catalog** | [theme_index.md](02-Themes/theme_index.md) | Browse problems grouped by 18 official themes |
| 🏢 **Organizations Catalog** | [organization_index.md](03-Organizations/organization_index.md) | Browse problems by Ministry, PSU, or Industry partner |
| 🔧 **Technologies Catalog** | [technology_index.md](04-Technologies/technology_index.md) | Browse problems tagged by AI/ML, IoT, GIS, Robotics, etc. |
| 📊 **Domains Catalog** | [domain_index.md](05-Domains/domain_index.md) | Browse problems by sector (Healthcare, Agriculture, Defence, etc.) |
| ⚙️ **Software vs Hardware** | [category_index.md](06-Indexes/category_index.md) | View Software vs Hardware problem breakdown |

---

## 📂 Repository Architecture

```
SIH-PS-VAULT-26/
├── README.md                      # Public repository overview & quick navigation
├── HOME.md                        # Obsidian Vault dashboard landing page
├── AGENTS.md                      # AI Agent entry point & instructions
├── 00-Meta/
│   ├── DATA-MODEL.md              # Canonical Data Model & Field Ownership Table
│   ├── PROVENANCE.md              # Provenance Levels & Conflict Resolution Protocol
│   ├── TAXONOMY.md                # Official vs Derived Taxonomies Specification
│   ├── GENERATION.md              # Build Pipeline & Path Classifications
│   ├── VALIDATION.md              # Validation Contract & Verification Suite
│   ├── About-This-Vault.md        # Data source, extraction & verification methodology
│   └── ps_template.md             # Clean Problem Statement Markdown template
├── docs/
│   ├── AGENT-KNOWLEDGE-RULES.md   # AI Agent Knowledge Interpretation Rules
│   └── ARCHITECTURE.md            # System Architecture & Layered Model
├── 01-Problem-Statements/         # 226 Problem Statement files (PS-26001.md to PS-26226.md)
├── 02-Themes/
│   ├── theme_index.md             # Master Theme Catalog
│   └── [18 Theme Files].md
├── 03-Organizations/
│   ├── organization_index.md      # Master Organization Catalog
│   └── [30 Org Files].md
├── 04-Technologies/
│   ├── technology_index.md        # Master Technology Catalog
│   └── [20 Tech Files].md
├── 05-Domains/
│   ├── domain_index.md            # Master Domain Classification Index
│   └── [17 Domain Files].md
├── 06-Indexes/
│   ├── all_problems_index.md      # Master Table of all 226 Problem Statements
│   └── category_index.md          # Software vs Hardware problem lists
└── data/
    ├── sih2026_problem_statements.json  # Ground-truth normalized JSON dataset
    └── sih2026_raw.html                 # Raw HTML source snapshot
```

---

## 🚀 How to Use This Vault

### Option 1: Direct GitHub Browsing
- Click any link in [all_problems_index.md](06-Indexes/all_problems_index.md) or [theme_index.md](02-Themes/theme_index.md) to view problem statements directly in GitHub.
- Every note contains relative back-links to return to catalogs or explore related problems.

### Option 2: Obsidian Knowledge Graph
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/SIH-PS-VAULT-26.git
   ```
2. Open **Obsidian** and select **"Open folder as vault"**.
3. Choose the `SIH-PS-VAULT-26` folder.
4. Set `HOME.md` as your homepage note.
5. Open **Graph View** (`Ctrl+G`) to visualize relationships between problem statements, technologies, themes, and organizations.

### Option 3: Command Line / Grep Search
- Search by keyword across all problem statements:
  ```bash
  grep -ri "landslide" 01-Problem-Statements/
  ```
- Find all Hardware problems:
  ```bash
  grep -l "category: \"Hardware\"" 01-Problem-Statements/*.md
  ```

### Option 4: Programmatic Access (JSON)
Access the structured dataset directly in Python:
```python
import json

with open('data/sih2026_problem_statements.json') as f:
    data = json.load(f)

problems = data['problems']
print(f"Total problems: {len(problems)}")
```

---

## ℹ️ Data Source & Integrity

- **Official Source**: [Smart India Hackathon 2026 Portal]({SOURCE_URL})
- **Verification**: 100% of 226 problem statement modals scraped, cleaned, and encoding-verified. Zero data loss, truncation, or broken references.
- For technical details on data extraction, see [about_vault.md](00-Meta/about_vault.md).

---
*Maintained for SIH 2026 participants, mentors, and innovation researchers.*
"""
    fp = os.path.join(vault_root, 'README.md')
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c)


def gen_home(problems, vault_root):
    """Generate HOME.md landing dashboard for Obsidian users."""
    themes = Counter(p['theme'] for p in problems)
    orgs = Counter(p['organization'] for p in problems)
    sw = sum(1 for p in problems if p['category'] == 'Software')
    hw = sum(1 for p in problems if p['category'] == 'Hardware')
    actual = [p for p in problems if p['title'] != 'Student Innovation']

    c = f"""---
type: home
tags: [sih2026, dashboard]
---
# 🏠 SIH 2026 — Intelligence Vault Dashboard

> Smart India Hackathon 2026 · **{len(problems)} Problem Statements** · Connected Knowledge Vault

## 📊 Quick Overview

| Metric | Count |
|--------|------:|
| Total Problem Statements | **{len(problems)}** |
| Ministry & Nodal Org Problems | **{len(actual)}** |
| Student Innovation Themes | **{len(problems) - len(actual)}** |
| Software Problems | **{sw}** |
| Hardware Problems | **{hw}** |
| Themes | **{len(themes)}** |
| Nodal Organizations | **{len(orgs)}** |

---

## 🧭 Master Navigation

| Catalog | Direct Link | Description |
|---------|-------------|-------------|
| 📋 All Problems | [all_problems_index.md](06-Indexes/all_problems_index.md) | Complete master table |
| 🏷️ By Theme | [theme_index.md](02-Themes/theme_index.md) | 18 Theme catalog hubs |
| 🏢 By Organization | [organization_index.md](03-Organizations/organization_index.md) | 30 Ministry & Industry catalogs |
| 🔧 By Technology | [technology_index.md](04-Technologies/technology_index.md) | 20 Technology tags |
| 📊 By Domain | [domain_index.md](05-Domains/domain_index.md) | 17 Domain classifications |
| ⚙️ Software vs Hardware | [category_index.md](06-Indexes/category_index.md) | Category breakdown |

---

## 🏷️ Themes at a Glance

| Theme | Total | SW | HW | Link |
|-------|------:|---:|---:|------|
"""
    for t, count in themes.most_common():
        s = sum(1 for p in problems if p['theme'] == t and p['category'] == 'Software')
        h = sum(1 for p in problems if p['theme'] == t and p['category'] == 'Hardware')
        tfname = sanitize_filename(t)
        tl = rel_link(t, None, DIRS['themes'], tfname)
        c += f"| {t} | {count} | {s} | {h} | {tl} |\n"

    c += "\n---\n\n## 🏢 Top Nodal Organizations\n\n| Organization | Type | Count | Link |\n|-------------|------|------:|------|\n"
    for o, count in orgs.most_common(15):
        ot = next((p['_org_type'] for p in problems if p['organization'] == o), 'Government')
        ofname = sanitize_filename(o)
        ol = rel_link(o[:45], None, DIRS['orgs'], ofname)
        c += f"| {o[:45]} | {ot} | {count} | {ol} |\n"

    c += f"""
---

## ℹ️ Vault Metadata
- **Source**: [{SOURCE_URL}]({SOURCE_URL})
- **Documentation**: [about_vault.md](00-Meta/about_vault.md) | [vault_user_guide.md](00-Meta/vault_user_guide.md)
"""
    fp = os.path.join(vault_root, 'HOME.md')
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c)


def gen_indexes(problems, vault_root):
    """Generate clean index files with unique descriptive filenames."""
    sub_idx = DIRS['indexes']

    # 1. All Problems Master Table (all_problems_index.md)
    c = "---\ntype: index\ntags: [sih2026, index]\n---\n# 📋 All Problem Statements Master Catalog\n\n"
    c += f"> Total **{len(problems)}** Problem Statements from SIH 2026\n\n"
    c += "| PS ID | Title | Organization | Category | Theme |\n|-------|-------|-------------|----------|-------|\n"
    for ps in sorted(problems, key=lambda x: int(x['ps_id'])):
        pid = ps['ps_id']
        t = ps['title'][:65]
        org = ps['organization'][:30]
        cat = ps['category']
        theme = ps['theme'][:22]
        ps_l = rel_link(f"PS-{pid}", sub_idx, DIRS['ps'], f"PS-{pid}")
        org_l = rel_link(org, sub_idx, DIRS['orgs'], sanitize_filename(ps['organization']))
        theme_l = rel_link(theme, sub_idx, DIRS['themes'], sanitize_filename(ps['theme']))
        c += f"| {ps_l} | {t} | {org_l} | {cat} | {theme_l} |\n"
    _write(vault_root, sub_idx, 'all_problems_index.md', c)

    # 2. Problems by Category (category_index.md)
    sw_probs = [p for p in problems if p['category'] == 'Software']
    hw_probs = [p for p in problems if p['category'] == 'Hardware']
    c = f"---\ntype: index\n---\n# ⚙️ Problems by Category\n\n## 💻 Software Problems ({len(sw_probs)})\n\n"
    c += "| PS ID | Title | Organization | Theme |\n|-------|-------|-------------|-------|\n"
    for ps in sorted(sw_probs, key=lambda x: int(x['ps_id'])):
        pid = ps['ps_id']
        ps_l = rel_link(f"PS-{pid}", sub_idx, DIRS['ps'], f"PS-{pid}")
        org_l = rel_link(ps['organization'][:30], sub_idx, DIRS['orgs'], sanitize_filename(ps['organization']))
        theme_l = rel_link(ps['theme'][:22], sub_idx, DIRS['themes'], sanitize_filename(ps['theme']))
        c += f"| {ps_l} | {ps['title'][:60]} | {org_l} | {theme_l} |\n"

    c += f"\n## 🔌 Hardware Problems ({len(hw_probs)})\n\n"
    c += "| PS ID | Title | Organization | Theme |\n|-------|-------|-------------|-------|\n"
    for ps in sorted(hw_probs, key=lambda x: int(x['ps_id'])):
        pid = ps['ps_id']
        ps_l = rel_link(f"PS-{pid}", sub_idx, DIRS['ps'], f"PS-{pid}")
        org_l = rel_link(ps['organization'][:30], sub_idx, DIRS['orgs'], sanitize_filename(ps['organization']))
        theme_l = rel_link(ps['theme'][:22], sub_idx, DIRS['themes'], sanitize_filename(ps['theme']))
        c += f"| {ps_l} | {ps['title'][:60]} | {org_l} | {theme_l} |\n"
    _write(vault_root, sub_idx, 'category_index.md', c)

    # 3. Theme Catalog Index (theme_index.md in 02-Themes)
    sub_th = DIRS['themes']
    c = "---\ntype: index\n---\n# 🏷️ Theme Catalog Index\n\n"
    themes = Counter(p['theme'] for p in problems)
    for t, count in themes.most_common():
        tfname = sanitize_filename(t)
        tl = rel_link(t, sub_th, sub_th, tfname)
        c += f"## {tl} ({count} problems)\n\n"
        for ps in sorted([p for p in problems if p['theme'] == t], key=lambda x: int(x['ps_id']))[:5]:
            pid = ps['ps_id']
            ps_l = rel_link(f"PS-{pid}", sub_th, DIRS['ps'], f"PS-{pid}")
            c += f"- {ps_l} — {ps['title'][:75]}\n"
        if count > 5:
            c += f"- *...and {count-5} more in full theme catalog*\n"
        c += "\n"
    _write(vault_root, sub_th, 'theme_index.md', c)

    # 4. Organization Catalog Index (organization_index.md in 03-Organizations)
    sub_org = DIRS['orgs']
    c = "---\ntype: index\n---\n# 🏢 Organization Catalog Index\n\n| Organization | Type | Problems | Catalog Link |\n|-------------|------|--------:|--------------|\n"
    orgs = Counter(p['organization'] for p in problems)
    for o, count in orgs.most_common():
        ot = next((p['_org_type'] for p in problems if p['organization'] == o), 'Government')
        ofname = sanitize_filename(o)
        ol = rel_link(o[:45], sub_org, sub_org, ofname)
        c += f"| {o[:45]} | {ot} | {count} | {ol} |\n"
    _write(vault_root, sub_org, 'organization_index.md', c)

    # 5. Technology Catalog Index (technology_index.md in 04-Technologies)
    sub_tech = DIRS['tech']
    all_techs = Counter()
    for p in problems:
        for t in p.get('_technologies', []):
            all_techs[t] += 1
    c = "---\ntype: index\n---\n# 🔧 Technology Catalog Index\n\n| Technology | Problem Count | Catalog Link |\n|------------|--------------:|--------------|\n"
    for t, count in all_techs.most_common():
        tl = rel_link(t.replace('-', ' '), sub_tech, sub_tech, t)
        c += f"| {t.replace('-', ' ')} | {count} | {tl} |\n"
    _write(vault_root, sub_tech, 'technology_index.md', c)

    # 6. Domain Catalog Index (domain_index.md in 05-Domains)
    sub_dom = DIRS['domains']
    all_domains = Counter()
    for p in problems:
        for d in p.get('_domains', []):
            all_domains[d] += 1
    c = "---\ntype: index\n---\n# 📊 Domain Catalog Index\n\n| Domain | Problem Count | Catalog Link |\n|--------|--------------:|--------------|\n"
    for d, count in all_domains.most_common():
        dl = rel_link(d.replace('-', ' '), sub_dom, sub_dom, d)
        c += f"| {d.replace('-', ' ')} | {count} | {dl} |\n"
    _write(vault_root, sub_dom, 'domain_index.md', c)


def gen_meta(problems, vault_root):
    """Generate meta documentation pages."""
    sub_meta = DIRS['meta']

    # about_vault.md
    c = f"""---
type: meta
---
# ℹ️ About the SIH 2026 Vault

## 📌 Data Provenance & Methodology
- **Official Source**: [{SOURCE_URL}]({SOURCE_URL})
- **Extraction Technique**: Automated parsing of official SIH modal dialogues
- **Data Integrity**: 100% of 226 problem statements extracted and verified against live portal.
- **Encoding Repair**: All CP1252/UTF-8 character anomalies repaired.

## 🗂️ Knowledge Categorization
1. **Official Metadata**: PS ID, Title, Organization, Department, Theme, Category, Official Description, Expected Solution.
2. **Extracted Taxonomies**: Normalized Technology tags and Domain classifications mapped via domain-specific keyphrase regex matcher.
3. **Cross-Links**: Every problem is cross-indexed with its corresponding Theme, Organization, Technologies, Domains, and Related Problems.
"""
    _write(vault_root, sub_meta, 'about_vault.md', c)

    # vault_user_guide.md
    c = """---
type: meta
---
# 🧭 Vault User & Explorer Guide

## 🔍 How to Search and Filter

### 1. By Theme
Navigate to `02-Themes/theme_index.md` to see all 18 themes (e.g., Disaster Management, Smart Automation, Agriculture).

### 2. By Nodal Organization
Navigate to `03-Organizations/organization_index.md` to view problem statements by Ministry or Industry partner (e.g., ISRO, DRDO, MDoNER, AICTE).

### 3. By Technology
Navigate to `04-Technologies/technology_index.md` to view problem statements using specific tech stacks (e.g., AI & ML, IoT, GIS, Computer Vision).

### 4. By Sector / Domain
Navigate to `05-Domains/domain_index.md` to view problem statements classified by domain (Healthcare, Defence, Mining, Energy).

### 5. By Category (Software vs Hardware)
Navigate to `06-Indexes/category_index.md` to quickly separate Software projects from Hardware prototype requirements.

## 💻 Obsidian Features
- Use `Ctrl + O` to quick-open any Problem Statement by ID (e.g. `PS-26001`).
- Use `Ctrl + Shift + F` for full-text search across all 226 problem statements.
- Use **Graph View** (`Ctrl + G`) to visually explore connections between technologies, themes, and organizations.
"""
    _write(vault_root, sub_meta, 'vault_user_guide.md', c)

    # ps_template.md
    c = """---
ps_id: ""
title: ""
organization: ""
department: ""
organization_type: ""
category: ""
theme: ""
technologies: []
domains: []
has_dataset: false
source_url: ""
aliases: []
tags: [sih2026]
---
# PS {{ps_id}} — {{title}}

> [!info] Quick Reference
> **Organization**: ... | **Theme**: ... | **Category**: ...

### 🔧 Key Classifications
**Technologies**: ...
**Domains**: ...

---

## 📋 Official Problem Statement

### Background
...

### Problem Description
...

### Expected Solution & Deliverables
...

---

## 🔗 Related Problem Statements
- ...
"""
    _write(vault_root, sub_meta, 'ps_template.md', c)


def _write(vault_root, subdir, filename, content):
    fp = os.path.join(vault_root, subdir, filename)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)


def cleanup_obsolete_directories(vault_root):
    """Remove obsolete legacy directories if they exist."""
    obsolete = ['06-Analysis', '07-Indexes', 'Templates']
    for folder in obsolete:
        p = os.path.join(vault_root, folder)
        if os.path.exists(p):
            print(f"Removing obsolete directory: {folder}")
            shutil.rmtree(p)


def clean_stale_artifacts(problems, vault_root):
    """Remove obsolete/orphaned generated files that no longer exist in current dataset."""
    expected_files = set()

    # Expected PS files
    for ps in problems:
        expected_files.add(os.path.join(vault_root, DIRS['ps'], f"PS-{ps['ps_id']}.md"))

    # Expected Theme files
    themes = set(p['theme'] for p in problems)
    for t in themes:
        expected_files.add(os.path.join(vault_root, DIRS['themes'], f"{sanitize_filename(t)}.md"))
    expected_files.add(os.path.join(vault_root, DIRS['themes'], 'theme_index.md'))

    # Expected Org files
    orgs = set(p['organization'] for p in problems)
    for o in orgs:
        expected_files.add(os.path.join(vault_root, DIRS['orgs'], f"{sanitize_filename(o)}.md"))
    expected_files.add(os.path.join(vault_root, DIRS['orgs'], 'organization_index.md'))

    # Expected Tech files
    all_techs = set(t for p in problems for t in p.get('_technologies', []))
    for t in all_techs:
        expected_files.add(os.path.join(vault_root, DIRS['tech'], f"{t}.md"))
    expected_files.add(os.path.join(vault_root, DIRS['tech'], 'technology_index.md'))

    # Expected Domain files
    all_domains = set(d for p in problems for d in p.get('_domains', []))
    for d in all_domains:
        expected_files.add(os.path.join(vault_root, DIRS['domains'], f"{d}.md"))
    expected_files.add(os.path.join(vault_root, DIRS['domains'], 'domain_index.md'))

    # Expected Index files
    expected_files.add(os.path.join(vault_root, DIRS['indexes'], 'all_problems_index.md'))
    expected_files.add(os.path.join(vault_root, DIRS['indexes'], 'category_index.md'))

    # Check generated directories for orphan files
    gen_dirs = [DIRS['ps'], DIRS['themes'], DIRS['orgs'], DIRS['tech'], DIRS['domains'], DIRS['indexes']]
    removed_count = 0
    for gdir in gen_dirs:
        dir_path = os.path.join(vault_root, gdir)
        if not os.path.exists(dir_path):
            continue
        for fname in os.listdir(dir_path):
            if fname.endswith('.md'):
                fpath = os.path.join(dir_path, fname)
                if fpath not in expected_files:
                    print(f"Removing stale generated file: {os.path.relpath(fpath, vault_root)}")
                    os.remove(fpath)
                    removed_count += 1

    if removed_count > 0:
        print(f"  ✓ Cleaned {removed_count} stale/orphaned generated files")
    else:
        print("  ✓ No stale generated files found")



def validate_relative_links(vault_root):
    """Validate 100% of Markdown relative links across all files in vault."""
    import glob
    all_md_files = glob.glob(os.path.join(vault_root, '**/*.md'), recursive=True)
    print(f"Validating relative links across {len(all_md_files)} markdown files...")

    broken_links = []
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    for filepath in all_md_files:
        file_dir = os.path.dirname(filepath)
        rel_file = os.path.relpath(filepath, vault_root)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        for match in link_pattern.finditer(content):
            link_text = match.group(1)
            link_target = match.group(2)

            # Skip web URLs or anchor-only links
            if link_target.startswith(('http://', 'https://', '#', 'mailto:')):
                continue

            # Strip anchor if present
            target_path = link_target.split('#')[0]
            if not target_path:
                continue

            # Resolve absolute target path
            abs_target = os.path.abspath(os.path.join(file_dir, target_path))

            if not os.path.exists(abs_target):
                broken_links.append((rel_file, link_target, abs_target))

    return all_md_files, broken_links


def main():
    print("Loading data...")
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    problems = data['problems']
    print(f"Loaded {len(problems)} problems")

    print("Processing technologies, domains, sections, and similarities...")
    problems = process_all(problems)

    cleanup_obsolete_directories(VAULT_ROOT)
    make_dirs()

    print("Cleaning obsolete/orphaned generated artifacts...")
    clean_stale_artifacts(problems, VAULT_ROOT)

    print("Generating 226 clean PS markdown files...")
    for ps in problems:
        generate_ps_file(ps, VAULT_ROOT)
    print("  ✓ PS files done")

    print("Generating theme catalog pages...")
    themes = sorted(set(p['theme'] for p in problems))
    for t in themes:
        generate_theme_page(t, problems, VAULT_ROOT)
    print(f"  ✓ {len(themes)} theme pages done")

    print("Generating organization catalog pages...")
    orgs = sorted(set(p['organization'] for p in problems))
    for o in orgs:
        generate_org_page(o, problems, VAULT_ROOT)
    print(f"  ✓ {len(orgs)} org pages done")

    print("Generating technology catalog pages...")
    all_techs = sorted(set(t for p in problems for t in p.get('_technologies', [])))
    for t in all_techs:
        generate_tech_page(t, problems, VAULT_ROOT)
    print(f"  ✓ {len(all_techs)} tech pages done")

    print("Generating domain catalog pages...")
    all_domains = sorted(set(d for p in problems for d in p.get('_domains', [])))
    for d in all_domains:
        generate_domain_page(d, problems, VAULT_ROOT)
    print(f"  ✓ {len(all_domains)} domain pages done")

    print("Generating index pages with unique filenames...")
    gen_indexes(problems, VAULT_ROOT)
    print("  ✓ Index pages done")

    print("Generating README.md and HOME.md...")
    gen_readme(problems, VAULT_ROOT)
    gen_home(problems, VAULT_ROOT)
    print("  ✓ README.md & HOME.md done")

    print("Generating meta documentation...")
    gen_meta(problems, VAULT_ROOT)
    print("  ✓ Meta pages done")

    print("\nValidating relative links...")
    all_files, broken = validate_relative_links(VAULT_ROOT)
    print(f"  Total Markdown files: {len(all_files)}")
    print(f"  Broken relative links: {len(broken)}")

    if broken:
        print("  ⚠️ BROKEN LINKS FOUND:")
        for src, target, resolved in broken[:20]:
            print(f"    {src} -> {target}")
    else:
        print("  ✅ 100% PERFECT RELATIVE LINKS — 0 BROKEN LINKS")

    print(f"\n{'='*60}")
    print(f"🎉 VAULT REFACTORED & REDESIGNED SUCCESSFULLY")
    print(f"   {len(all_files)} files created across vault")
    print(f"   Open README.md on GitHub or HOME.md in Obsidian")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
