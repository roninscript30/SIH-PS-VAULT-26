# Generation Pipeline & Build Contract

> **SIH PS Vault 2026** · Vault Generation, Build Orchestration & Stale Artifact Specification

---

## 1. Pipeline Overview

The **SIH PS Vault** build pipeline transforms normalized problem statement JSON data into an offline-ready, hyperlinked Obsidian knowledge vault.

```
┌──────────────────────────────────────┐
│       Raw Portal HTML Snapshot       │ (data/sih2026_raw.html)
└──────────────────┬───────────────────┘
                   │
                   ▼ [verify_data.py / scraper.py]
┌──────────────────────────────────────┐
│  Canonical Ground-Truth JSON Dataset  │ (data/sih2026_problem_statements.json)
└──────────────────┬───────────────────┘
                   │
                   ▼ [vault_processor.py: extract techs, domains, sections, similarities]
┌──────────────────────────────────────┐
│        Metadata Enrichment           │ (In-memory enriched structure)
└──────────────────┬───────────────────┘
                   │
                   ▼ [generate_vault.py / vault_generators.py]
┌────────────────────────────────────────────────────────────────────────┐
│                          Vault Generation Renders                      │
├──────────────────┬───────────────────┬────────────────┬────────────────┤
│ 01-Problem-Stmts │ 02-Themes & Orgs  │ 04-Tech & Dom  │ 06-Indexes &   │
│   (226 PS notes) │   (Catalog hubs)  │ (Concept tags) │ README / HOME  │
└──────────────────┴───────────────────┴────────────────┴────────────────┘
                   │
                   ▼ [verify_data.py]
┌──────────────────────────────────────┐
│      100% Validation Verification    │ (0 broken links, 226 PS matched)
└──────────────────────────────────────┘
```

---

## 2. Directory & Path Classifications

To guarantee reproducibility and prevent source-of-truth conflicts, every file and folder in the repository belongs to one of four operational classifications:

| Path / Folder | Classification | Modifiable Manually? | Description / Cleanup Rule |
| :--- | :--- | :---: | :--- |
| `data/sih2026_raw.html` | **SOURCE** | ❌ No | Raw local source snapshot from live portal |
| `data/sih2026_problem_statements.json` | **SOURCE (Canonical)** | ❌ No | Ground-truth normalized JSON dataset |
| `01-Problem-Statements/*.md` | **GENERATED** | ❌ No | 226 individual problem statement notes |
| `02-Themes/*.md` | **GENERATED** | ❌ No | 18 Theme catalog pages + `theme_index.md` |
| `03-Organizations/*.md` | **GENERATED** | ❌ No | 30 Organization hub pages + `organization_index.md` |
| `04-Technologies/*.md` | **GENERATED** | ❌ No | 20 Technology catalog pages + `technology_index.md` |
| `05-Domains/*.md` | **GENERATED** | ❌ No | 17 Domain classification pages + `domain_index.md` |
| `06-Indexes/*.md` | **GENERATED** | ❌ No | Master indices (`all_problems_index.md`, `category_index.md`) |
| `00-Meta/*` | **MANUAL** | ✅ Yes | Architecture, provenance, taxonomy, and guide specs |
| `docs/*` | **MANUAL** | ✅ Yes | System architecture, agent rules, and reports |
| `README.md` | **MANUAL / GENERATED** | ✅ Yes | Repository landing page & user guide |
| `HOME.md` | **MANUAL / GENERATED** | ✅ Yes | Obsidian dashboard landing page |
| `scripts/vault_config.py` | **CONFIGURATION** | ✅ Yes | Keyphrase lists, folder definitions, org mappings |
| `scripts/*.py` | **CONFIGURATION** | ✅ Yes | Pipeline orchestrators, processors, and validators |
| `.obsidian/*` | **CONFIGURATION** | ✅ Yes | Shared portable Obsidian workspace settings |

---

## 3. Pipeline Components & Roles

The generation pipeline relies on four modular scripts located in `scripts/`:

1. **`scripts/vault_config.py` (Configuration)**:
   - Defines directory constants (`DIRS`), file paths, keyphrase regex tables (`TECH_KEYWORDS`, `DOMAIN_KEYWORDS`), organization types (`ORG_TYPES`), and relative linking utilities (`rel_link`).
2. **`scripts/vault_processor.py` (Data Processor)**:
   - Performs regex keyphrase extraction (`extract_technologies`, `extract_domains`).
   - Parses official problem description into structured sections (`Background`, `Problem Description`, `Expected Solution`).
   - Computes multi-attribute similarity scores to link related problems (`detect_similarities`).
3. **`scripts/vault_generators.py` (Render Generators)**:
   - Renders individual Markdown notes (`generate_ps_file`) with YAML frontmatter, callout boxes, and relative links.
   - Renders catalog hub pages for Themes, Organizations, Technologies, and Domains.
4. **`scripts/generate_vault.py` (Main Orchestration Engine)**:
   - Loads JSON dataset, triggers processor enrichment, executes safe stale file cleanup, invokes generators, builds master indices, `README.md`, and `HOME.md`, and runs immediate link integrity checks.

---

## 4. Stale Artifact Cleanup Specification

To prevent orphaned or outdated Markdown files when the underlying dataset changes:
- `generate_vault.py` executes `clean_stale_artifacts(problems, vault_root)`.
- It computes the exact set of expected file paths across `01-Problem-Statements/`, `02-Themes/`, `03-Organizations/`, `04-Technologies/`, `05-Domains/`, and `06-Indexes/`.
- Any existing `.md` file inside these generated directories that is not in the expected set is automatically removed.

---

## 5. Execution & Regeneration Commands

All operations can be executed from the repository root:

```bash
# 1. Regenerate complete vault from ground-truth JSON dataset
python3 scripts/generate_vault.py

# 2. Run single comprehensive verification suite
python3 scripts/verify_data.py
```

> [!IMPORTANT]
> **Manual Editing Rule**: Never manually edit files inside generated directories (`01-Problem-Statements/`, `02-Themes/`, `03-Organizations/`, `04-Technologies/`, `05-Domains/`, `06-Indexes/`). Any manual edits will be overwritten during the next run of `generate_vault.py`.
