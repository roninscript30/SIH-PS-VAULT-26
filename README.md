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

| Analysis Dimension | 🌐 Official SIH Web Portal | ⚡ SIH PS Vault 2026 (This Repo) |
| :--- | :--- | :--- |
| **Reading Experience** | Isolated modal popups on fragile web pages | **Hyperlinked Knowledge Graph & Relational Markdown** |
| **Cross-Ministry Analysis** | Manual scrolling across 226 separate listings | **Instant Cross-Catalog Synthesis (Themes, Orgs, Domains)** |
| **AI / NLP Compatibility** | ❌ Fails (Requires scraping, fails on dynamic UI) | **✅ Native NLP Ready (Clean Markdown + JSON Ground Truth)** |
| **Technical Extraction** | Raw unstructured text paragraphs | **Structured YAML Metadata (Tech Stack, Category, Ministry)** |
| **Offline Research** | Impossible (Requires active internet & portal uptime) | **100% Offline-Ready & Version-Controlled** |

---

## 💎 How to Use with Obsidian (Knowledge Graph View)

Visualize relationships across problem statements, nodal ministries, and technology domains in an interactive node network.

![Obsidian Knowledge Graph](00-Meta/obsidian_graph.png)

### Quick Setup
1. **Clone Repository**:
   ```bash
   git clone https://github.com/roninscript30/SIH-PS-VAULT-26.git
   ```
2. **Open in Obsidian**: Launch Obsidian ➔ **"Open folder as vault"** ➔ Select `SIH-PS-VAULT-26`.
3. **Launch Graph View**: Press `Ctrl+G` (or `Cmd+G` on macOS) to explore interactive connections.

---

## 🤖 Analyzing Problem Statements with AI Agents (NLP Prompts)

Instead of searching paths, use natural language NLP prompts to ask AI agents (**Claude Code**, **Codex**, **Antigravity**) to perform deep analysis, requirement extraction, architectural drafting, and technical feasibility scoring.

### 1. 🤖 Claude Code (Natural Language Analysis & Architecture Prompt)
> *"Analyze problem statement `PS-26001.md`. Extract its key operational constraints, target end-users, required sensor/data feeds, and offline sync requirements. Then generate a high-level system architecture, database schema, and tech stack recommendation."*

### 2. ⚡ OpenAI Codex (Cross-Problem Trend & Tech Stack Analysis)
> *"Perform an NLP analysis of `data/sih2026_problem_statements.json`. Identify all problem statements under 'Disaster Management', extract recurring technical requirements (such as GIS mapping, IoT sensors, or real-time alerts), and generate a comparative summary of required backend APIs."*

### 3. 🌌 Antigravity (Deep Pair-Programming & Solution Generation)
> *"Read `PS-26014.md` (Integrated GIS Land Governance) and synthesize a production solution. Create a React component structure, outline the REST API endpoints, and generate a step-by-step hackathon execution roadmap."*

---

## 💡 Prompt Harness Efficiency & Knowledge Base Strategy

Maximize AI agent intelligence and token efficiency using pre-structured knowledge:

- **NLP Requirement Extraction**: Prompt LLMs to extract core problem hooks, deliverables, and evaluation criteria directly from frontmatter tags.
- **Context-Stuffed Reasoning**: Provide agents with clean `.md` files or `data/sih2026_problem_statements.json` to eliminate hallucinations and achieve 10x faster synthesis.
- **Cross-Domain Ideation**: Combine technology nodes (e.g. `04-Technologies/AI-and-ML.md`) with domain nodes (e.g. `05-Domains/Agriculture.md`) to generate unique hackathon solution proposals.

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
├── README.md                      # Vault overview, comparison, Obsidian & AI Agent NLP guide
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
