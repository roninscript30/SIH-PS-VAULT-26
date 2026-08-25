# Phase 2 Knowledge Model & Architecture Specification Report

> **SIH PS Vault 2026** · Phase 2 Formal Knowledge Architecture Report

---

## 1. What Was Defined

Phase 2 established a formal, machine-readable, and human-verifiable **Knowledge Architecture & Contract** for the **SIH PS Vault**.

Seven core specification contracts and documentation artifacts were created:
1. [`00-Meta/DATA-MODEL.md`](../00-Meta/DATA-MODEL.md): Canonical entity model, field ownership table, and relationship semantics.
2. [`00-Meta/PROVENANCE.md`](../00-Meta/PROVENANCE.md): 5-level provenance classification, authority hierarchy, and conflict resolution protocols.
3. [`00-Meta/TAXONOMY.md`](../00-Meta/TAXONOMY.md): Specification of official vs. derived taxonomies and regex classifier rules.
4. [`00-Meta/GENERATION.md`](../00-Meta/GENERATION.md): Pipeline build stages, path classifications, and stale artifact cleanup rules.
5. [`00-Meta/VALIDATION.md`](../00-Meta/VALIDATION.md): Automated verification suite specification and audit report schema.
6. [`docs/AGENT-KNOWLEDGE-RULES.md`](AGENT-KNOWLEDGE-RULES.md): AI agent retrieval hierarchy, trust levels, citation standards, and safety rules.
7. [`docs/ARCHITECTURE.md`](ARCHITECTURE.md): Layered architectural model separating current implementation from future extensions.

---

## 2. Canonical Data Model

- **Core Entity**: Problem Statement (PS).
- **Identity**: `ps_id` (`26001`-`26226`), `title`, `source_url`.
- **Official Metadata**: `organization`, `department`, `category` (Software/Hardware), `theme` (18 official themes), `description` (`background`, `description`, `expected_solution`), `dataset_link`, `youtube_link`.
- **Derived Metadata**: `technologies` (20 tags), `domains` (17 sectors), `organization_type` (Government/Industry/PSU), `has_dataset`, `aliases`, `related_problems` (`_similar`).
- **Canonical Source of Truth**: `data/sih2026_problem_statements.json` is the canonical normalized dataset. `data/sih2026_raw.html` is the raw source snapshot. Markdown notes in `01-Problem-Statements/` are generated views.

---

## 3. Provenance Model

- **5 Provenance Levels**:
  1. `SOURCE`: Official portal text (100% authority, immutable by agents).
  2. `DERIVED`: Rule-based classifications (80-90% trust, regenerable).
  3. `GENERATED`: Rendered Markdown views and catalogs (100% regenerable).
  4. `ANALYSIS`: Evaluative heuristics and complexity scores.
  5. `RECOMMENDATION`: Proposed architectures, team matches, and solution ideas.
- **Authority Hierarchy**: Live Portal ➔ Raw Snapshot ➔ Normalized JSON ➔ Vault Markdown ➔ Indexes ➔ Downstream Inferences.
- **Golden Rule**: **NEVER SILENTLY OVERWRITE UNCERTAINTY**.

---

## 4. Taxonomy Model

- **Official Taxonomies**:
  - `Category`: 2 values (`Software`: 172, `Hardware`: 54).
  - `Theme`: 18 official SIH themes.
  - `Organization`: 30 nodal ministries, PSUs, and industry partners.
- **Derived Taxonomies**:
  - `Technologies`: 20 normalized keyphrase tags extracted via regex matching (`vault_config.py`).
  - `Domains`: 17 normalized sector classifications extracted via regex matching.
- **Derived Tag Disclaimer**: Technology and domain tags are derived analytics and must not be presented as official SIH classifications.

---

## 5. Generation Model

- **Deterministic Build Pipeline**: `SOURCE DATA` ➔ `NORMALIZATION` ➔ `PROBLEM STATEMENTS` ➔ `TAXONOMY` ➔ `INDEXES` ➔ `EXPORTS`.
- **Path Classifications**: Strictly partitions repository paths into `SOURCE`, `GENERATED`, `MANUAL`, and `CONFIGURATION`.
- **Stale Artifact Cleanup**: Automatically removes orphaned Markdown files in generated directories using dataset manifest matching (`clean_stale_artifacts`).

---

## 6. Validation Contract

- **Verification Tool**: Executable via `python3 scripts/verify_data.py`.
- **6 Check Categories**:
  1. Structural (226 PS count, continuous IDs `26001-26226`).
  2. Schema (JSON & YAML syntax compliance).
  3. Consistency (Source HTML ↔ JSON ↔ Markdown field matching).
  4. Relationship (100% valid relative links, 0 broken links across 333 files).
  5. Provenance (Official vs. derived separation).
  6. Generation (0 orphaned or stale files).
- **Report Output**: Machine-readable `data/verification_report.json`.

---

## 7. Agent Knowledge Rules

Future AI agents querying or reasoning over the vault must:
1. Prefer individual PS notes for source content and JSON dataset for structured filtering.
2. Explicitly categorize all reasoning into `FACT`, `DERIVED FACT`, `INFERENCE`, or `RECOMMENDATION`.
3. Provide explicit citations (`PS 26001`).
4. Preserve source uncertainty.
5. Modify generator scripts and JSON dataset instead of manually editing generated Markdown notes.

---

## 8. Current Architecture

```
Layer 1: Source Layer (Live Portal & sih2026_raw.html)
Layer 2: Normalization Layer (sih2026_problem_statements.json & scripts/vault_processor.py)
Layer 3: Knowledge Layer (01-Problem-Statements/*.md & 00-Meta/*.md)
Layer 4: Navigation Layer (02-Themes/, 03-Organizations/, 04-Technologies/, 05-Domains/, 06-Indexes/)
Layer 5: Agent Interface Layer (AGENTS.md & docs/AGENT-KNOWLEDGE-RULES.md)
```

---

## 9. Future Architecture (Planned)

```
Layer 6: Downstream Intelligence Layer [PLANNED]
  ├── Vector Embeddings & Indexing (ChromaDB / Qdrant)
  ├── Semantic Vector & Hybrid Search
  ├── Automated Feasibility & Evaluation Engine
  ├── Team & Skill Matching Subsystem
  └── RAG / Solution Generation Agents
```

---

## 10. Known Ambiguities

1. **Student Innovation Open Slots**: 34 problem statements represent open-ended AICTE innovation themes rather than specific ministry requirements.
2. **CP1252 Character Encoding Repair**: Raw HTML modals contained Windows-1252 mojibake artifacts (`â€™`, `â€œ`), which have been repaired to standard UTF-8 in the normalized dataset.
3. **Keyword Overlap**: Regex keyword matching can occasionally trigger false positives (e.g. `"train"` matching `"training model"`). Refinements are handled centrally in `scripts/vault_config.py`.

---

## 11. Decisions Deferred to Phase 3

The following technical implementations were intentionally deferred to future phases:
- Embedding model selection and vector database setup.
- RAG pipeline construction and semantic search APIs.
- AI problem feasibility scoring algorithms.
- Solution proposal generation and team matching workflows.
- Web application / REST API development.
