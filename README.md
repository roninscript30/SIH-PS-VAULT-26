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

## ⚖️ Problem Statement Analysis: Official Portal vs. SIH PS Vault

| Analysis & Selection Dimension | 🌐 Official SIH Web Portal | ⚡ SIH PS Vault 2026 (This Repo) |
| :--- | :--- | :--- |
| **Problem Discovery** | Click through 226 individual modal popups | **Instant Multi-Catalog Search & Skill-Based Filtering** |
| **Selection & Shortlisting** | Manual note-taking without filtering tools | **AI-Powered Multi-Criteria Evaluation & Ranking** |
| **Cross-Ministry Comparison** | Hard to compare requirements across ministries | **Instant Tech Stack & Domain Overlap Synthesis** |
| **AI Agent Ingestion** | ❌ Fails (Requires scraping dynamic UI) | **✅ Direct AI Context Ingestion (Markdown + JSON)** |
| **Offline Evaluation** | Impossible (Requires active portal connection) | **100% Offline-Ready & Version-Controlled** |

---

## 💎 How to Use with Obsidian (Knowledge Graph View)

Visually discover, explore, and select problem statements by mapping relationships across nodal ministries, themes, and technology stacks.

![Obsidian Knowledge Graph](00-Meta/obsidian_graph.png)

### Quick Setup
1. **Clone Repository**:
   ```bash
   git clone https://github.com/roninscript30/SIH-PS-VAULT-26.git
   ```
2. **Open in Obsidian**: Launch Obsidian ➔ **"Open folder as vault"** ➔ Select `SIH-PS-VAULT-26`.
3. **Launch Graph View**: Press `Ctrl+G` (or `Cmd+G` on macOS) to visually navigate nodes and select target problem statements.

---

## 🤖 Problem Statement Search, Discovery & Selection with AI Agents

Use natural language NLP prompts to ask AI agents (**Claude Code**, **Codex**, **Antigravity**) to search, evaluate, filter, and select the best hackathon problem statements for your team based on skill set, feasibility, and technical scope.

### 1. 🤖 Skill-Based Problem Discovery (Claude Code)
> *"Our team is skilled in Python, PyTorch, GIS mapping (Leaflet/Mapbox), and React. Scan all 226 problem statements in `01-Problem-Statements/` and recommend the top 3 Software problem statements that match our skill set, along with technical feasibility trade-offs for each."*

### 2. ⚡ Strategic Shortlisting & Impact Filtering (OpenAI Codex / GPT)
> *"Parse `data/sih2026_problem_statements.json` and shortlist all Software problems from Central Ministries (e.g., ISRO, MoES, DRDO, MDoNER) involving Computer Vision or NLP. Rank them by technical complexity, expected social impact, and clarity of deliverables."*

### 3. 🌌 Multi-Criteria Problem Selection (Antigravity)
> *"Compare all problem statements in `02-Themes/Disaster-Management.md` against `02-Themes/Smart-Automation.md`. Select the single best problem statement for a 36-hour hackathon, explaining why it wins in innovation hook, data availability, and prototype feasibility."*

---

## 💡 Smart Selection & Prompt Harness Strategy

Harness AI agents as decision-support engines to pick the winning problem statement:

- **Team-Skill Alignment**: Match your team's core competencies (Web, AI/ML, Hardware, Mobile) against frontmatter technology tags to avoid choosing out-of-scope problems.
- **Eliminate Risk Candidates**: Prompt AI agents to screen for problem statements that require unavailable proprietary datasets or complex hardware dependencies.
- **Cross-Domain Shortlisting**: Combine technology indices (e.g. `04-Technologies/GIS-and-Geospatial.md`) with domain indices (e.g. `05-Domains/Disaster-Response.md`) to find high-impact, low-competition challenges.

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
├── README.md                      # Vault overview, selection guide, Obsidian & AI Agent NLP guide
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
