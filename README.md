# 🇮🇳 Smart India Hackathon (SIH) 2026 — Problem Statement Vault

[![SIH 2026](https://img.shields.io/badge/SIH-2026-orange.svg)](https://www.sih.gov.in/sih2026PS)
[![Problem Statements](https://img.shields.io/badge/Problems-226-blue.svg)](06-Indexes/all_problems_index.md)
[![Software](https://img.shields.io/badge/Software-172-green.svg)](06-Indexes/category_index.md)
[![Hardware](https://img.shields.io/badge/Hardware-54-red.svg)](06-Indexes/category_index.md)
[![Themes](https://img.shields.io/badge/Themes-18-purple.svg)](02-Themes/theme_index.md)
[![Organizations](https://img.shields.io/badge/Organizations-30-yellow.svg)](03-Organizations/organization_index.md)

Welcome to the **Smart India Hackathon (SIH) 2026 Problem Statement Vault**. This repository provides an offline-ready, hyperlinked knowledge system containing all **226 official problem statements** released for SIH 2026.

Every problem statement has been cleaned, structured, and cross-indexed by **Theme**, **Organization**, **Technology**, **Domain**, and **Category** with 100% relative Markdown links for seamless navigation on GitHub or in Obsidian.

---

## 📊 Vault Quick Statistics

| Metric | Count | Description |
|--------|------:|-------------|
| **Total Problem Statements** | **226** | Complete official release |
| **Unique Ministry/Org Problems** | **192** | Targeted problem statements |
| **Student Innovation Slots** | **34** | Open-ended AICTE innovation themes |
| **Software Problems** | **172** | Web, Mobile, AI/ML, Cloud, GIS, Data platforms |
| **Hardware Problems** | **54** | Embedded systems, Robotics, Drones, IoT, Sensors |
| **Participating Themes** | **18** | Structured problem domains |
| **Nodal Organizations** | **30** | Central Ministries, PSUs, Industry leaders |

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
├── 00-Meta/
│   ├── about_vault.md             # Data source, extraction & verification methodology
│   ├── vault_user_guide.md        # Detailed guide on searching and exploring the vault
│   └── ps_template.md             # Clean Problem Statement Markdown template
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
    └── sih2026_problem_statements.json  # Raw verified JSON dataset
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
  grep -l "category: "Hardware"" 01-Problem-Statements/*.md
  ```

### Option 4: Programmatic Access (JSON)
Access the structured dataset directly in Python:
```python
import json

with open('data/sih2026_problem_statements.json') as f:
    data = json.load(f)

problems = data['problems']
print(f"Total problems: 226")
```

---

## ℹ️ Data Source & Integrity

- **Official Source**: [Smart India Hackathon 2026 Portal](https://www.sih.gov.in/sih2026PS)
- **Verification**: 100% of 226 problem statement modals scraped, cleaned, and encoding-verified. Zero data loss, truncation, or broken references.
- For technical details on data extraction, see [about_vault.md](00-Meta/about_vault.md).

---
*Maintained for SIH 2026 participants, mentors, and innovation researchers.*
