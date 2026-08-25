# Build and Generation Pipeline Guide

> **SIH PS Vault 2026** · Vault Build, Reproducibility & Stale Artifact Cleanup Specification

---

## 🗂️ Repository Directory & File Classifications

To guarantee reproducibility and clean maintenance boundaries, repository paths are classified into four distinct operational roles:

| Path / Folder | Classification | Modifiable Manually? | Description / Cleanup Rule |
| :--- | :--- | :---: | :--- |
| `data/sih2026_raw.html` | **SOURCE** | ❌ No | Raw local source snapshot from SIH portal |
| `data/sih2026_problem_statements.json` | **SOURCE** | ❌ No | Ground-truth normalized JSON dataset |
| `01-Problem-Statements/*.md` | **GENERATED** | ❌ No | 226 individual problem statement notes (Cleaned during generation) |
| `02-Themes/*.md` | **GENERATED** | ❌ No | 18 Theme catalog pages + `theme_index.md` (Cleaned during generation) |
| `03-Organizations/*.md` | **GENERATED** | ❌ No | 30 Organization hub pages + `organization_index.md` (Cleaned during generation) |
| `04-Technologies/*.md` | **GENERATED** | ❌ No | 20 Technology catalog pages + `technology_index.md` (Cleaned during generation) |
| `05-Domains/*.md` | **GENERATED** | ❌ No | 17 Domain classification pages + `domain_index.md` (Cleaned during generation) |
| `06-Indexes/*.md` | **GENERATED** | ❌ No | Master indices (`all_problems_index.md`, `category_index.md`) |
| `00-Meta/*` | **MANUAL** | ✅ Yes | Architecture, provenance, and guide documentation |
| `README.md` | **MANUAL / GENERATED** | ✅ Yes | Repository landing page & user guide |
| `HOME.md` | **MANUAL / GENERATED** | ✅ Yes | Obsidian dashboard landing page |
| `scripts/vault_config.py` | **CONFIGURATION** | ✅ Yes | Keyphrase lists, folder definitions, org mappings |
| `scripts/*.py` | **CONFIGURATION** | ✅ Yes | Pipeline orchestrators, processors, and validators |
| `.obsidian/*` | **CONFIGURATION** | ✅ Yes | Shared portable Obsidian workspace settings |

---

## 🔄 Vault Build Lifecycle & Reproducibility

Vault generation is 100% deterministic. Running the generation orchestrator rebuilds all generated files directly from `data/sih2026_problem_statements.json`.

### Build Workflow Steps:
1. **Load Source Data**: Read `data/sih2026_problem_statements.json`.
2. **Process Metadata**: Run `vault_processor.py` to extract technologies, domains, sections, and similar problem relationships.
3. **Safe Stale File Cleanup**: Clean obsolete files in generated subdirectories (`01-Problem-Statements/`, `02-Themes/`, `03-Organizations/`, `04-Technologies/`, `05-Domains/`, `06-Indexes/`).
4. **Regenerate Artifacts**: Generate clean Markdown notes, taxonomy catalogs, and master indices.
5. **Link Integrity Check**: Validate 100% of internal relative links.

---

## 🛠️ Execution Commands

All scripts can be executed directly from the repository root:

```bash
# 1. Regenerate complete vault from ground-truth JSON dataset
python scripts/generate_vault.py

# 2. Run single comprehensive verification suite
python scripts/verify_data.py
```
