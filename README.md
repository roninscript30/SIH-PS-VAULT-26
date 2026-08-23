# 🇮🇳 Smart India Hackathon (SIH) 2026 — Problem Statement Vault

[![SIH 2026](https://img.shields.io/badge/SIH-2026-orange.svg)](https://www.sih.gov.in/sih2026PS)
[![Problem Statements](https://img.shields.io/badge/Problems-226-blue.svg)](06-Indexes/all_problems_index.md)
[![Software](https://img.shields.io/badge/Software-172-green.svg)](06-Indexes/category_index.md)
[![Hardware](https://img.shields.io/badge/Hardware-54-red.svg)](06-Indexes/category_index.md)
[![Themes](https://img.shields.io/badge/Themes-18-purple.svg)](02-Themes/theme_index.md)
[![Organizations](https://img.shields.io/badge/Organizations-30-yellow.svg)](03-Organizations/organization_index.md)
[![JSON Dataset](https://img.shields.io/badge/Dataset-Verified_JSON-success.svg)](data/sih2026_problem_statements.json)

---

## 📌 What is SIH PS Vault?

> **The SIH PS Vault is the canonical, structured, version-controlled knowledge layer that preserves, organizes, indexes, and exposes SIH problem statements for human exploration, automated processing, research, AI/RAG, analytics, and downstream evaluation systems.**

This repository organizes all **226 official problem statements** of SIH 2026 into a clean, hyperlinked, offline-ready Markdown & JSON knowledge base.

---

## ⚖️ Why Use This Vault Instead of Official Web UI?

| Feature | 🌐 Official Web Portal | ⚡ SIH PS Vault 2026 |
| :--- | :---: | :---: |
| **Availability** | Online-only (Prone to downtime & slow modal popups) | **100% Offline, Lightning Fast** |
| **Exploration** | Linear paginated list | **Obsidian Knowledge Graph & Relational Links** |
| **Filtering** | Limited keyword search | **Filter by Tech Stack, Domain, Category & Org** |
| **AI Agent Ingestion** | ❌ Fails (Scraping required) | **✅ Instant Context Injection (Markdown + JSON)** |
| **Data Structure** | Raw HTML modal text | **Standardized YAML Frontmatter & JSON** |

---

## 💎 How to Use with Obsidian (Knowledge Graph View)

Experience an interactive visual network connecting problem statements, themes, nodal organizations, and technologies.

![Obsidian Knowledge Graph](00-Meta/obsidian_graph.png)

### Setup Instructions
1. **Clone Repository**:
   ```bash
   git clone https://github.com/roninscript30/SIH-PS-VAULT-26.git
   ```
2. **Open in Obsidian**: Launch Obsidian ➔ **"Open folder as vault"** ➔ Select `SIH-PS-VAULT-26`.
3. **Launch Graph View**: Press `Ctrl+G` (or `Cmd+G` on macOS) to visualize interactive node connections across problem statements, ministries, and tech stacks.

---

## 🤖 How to Use with AI Agents (Claude Code, Codex, Antigravity)

Using local Markdown files or JSON context instead of raw web text reduces prompt tokens by ~80% and eliminates web-scraping failures.

### 1. 🤖 Claude Code (CLI Agent)
```bash
# Query knowledge base directly for specific technology matches
claude "Search 01-Problem-Statements/ for 'GIS-and-Geospatial' and return top 3 software feasibility scores."

# Architectural breakdown prompt
claude "Read 01-Problem-Statements/PS-26001.md and generate a system architecture & database schema."
```

### 2. ⚡ OpenAI Codex & Script Pipelines
```python
import json

# Efficient Knowledge Base Querying
with open('data/sih2026_problem_statements.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Query problems matching specific requirements
ai_disaster_problems = [
    p for p in data['problems']
    if p['category'] == 'Software' and p['theme'] == 'Disaster Management'
]
print(f"Found {len(ai_disaster_problems)} Disaster Management software problems.")
```

### 3. 🌌 Antigravity (Google DeepMind Agent)
1. Open `SIH-PS-VAULT-26` workspace directory in Antigravity.
2. Direct Query Prompt:
   > *"Reference `06-Indexes/all_problems_index.md` and `04-Technologies/AI-and-ML.md`. Pick PS-26001 and create a full-stack web application prototype with Leaflet map rendering."*

---

## 💡 Prompt Harness Efficiency Strategy

To harness maximum agent efficiency when working with this vault:
- **Reference exact relative paths**: Pass file paths (e.g. `01-Problem-Statements/PS-26042.md`) directly in prompts instead of copying long text blocks.
- **Use Index Nodes for multi-problem queries**: Refer to `02-Themes/theme_index.md` or `04-Technologies/technology_index.md` for batch categorization tasks.

---

## 📊 Quick Statistics & Catalogs

| Metric | Count | Interactive Catalog Link |
| :--- | :---: | :--- |
| **Total Problems** | **226** | 📋 [all_problems_index.md](06-Indexes/all_problems_index.md) |
| **Software Problems** | **172** | ⚙️ [category_index.md](06-Indexes/category_index.md) |
| **Hardware Problems** | **54** | ⚙️ [category_index.md](06-Indexes/category_index.md) |
| **Themes** | **18** | 🏷️ [theme_index.md](02-Themes/theme_index.md) |
| **Organizations** | **30** | 🏢 [organization_index.md](03-Organizations/organization_index.md) |
| **Technologies** | **20** | 🔧 [technology_index.md](04-Technologies/technology_index.md) |
| **Domains** | **17** | 📊 [domain_index.md](05-Domains/domain_index.md) |

---

## 📂 Repository Architecture

```
SIH-PS-VAULT-26/
├── README.md                      # Vault overview, comparison, Obsidian & AI Agent guide
├── HOME.md                        # Obsidian Vault dashboard landing page
├── 00-Meta/
│   ├── About-This-Vault.md        # Data extraction methodology & lineage
│   ├── obsidian_graph.png         # Knowledge graph visual reference
│   └── vault_user_guide.md        # User navigation guide
├── 01-Problem-Statements/         # 226 Markdown notes (PS-26001.md to PS-26226.md)
├── 02-Themes/                     # 18 Theme catalog pages
├── 03-Organizations/              # 30 Organization hub pages
├── 04-Technologies/               # Technology index pages
├── 05-Domains/                    # Domain index pages
├── 06-Indexes/                    # Master indices (all problems, categories)
├── data/                          # Ground-truth verified JSON dataset
└── scripts/                       # Vault extraction, parsing & generation scripts
```

---

## ℹ️ Verified Data Integrity

- **Official Source**: [Smart India Hackathon 2026 Portal](https://www.sih.gov.in/sih2026PS)
- **Validation**: 100% verified (226/226 statements), UTF-8 cleaned, 0 truncation or missing fields.

---
*Maintained for SIH 2026 participants, mentors, AI agents, and innovation researchers.*
