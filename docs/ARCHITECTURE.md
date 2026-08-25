# System Architecture Specification

> **SIH PS Vault 2026** · High-Level Architecture, Layered System Model & System Boundaries

---

## 1. Executive Architecture Summary

The **SIH PS Vault** is a structured, offline-ready knowledge and data layer designed for human exploration (via Obsidian / GitHub) and machine/agent consumption.

The system is organized into **6 modular layers**, strictly partitioning raw source data, normalized representations, derived navigation indexes, and downstream intelligence interfaces.

---

## 2. Layered Architectural Model

```
=======================================================================
 CURRENTLY IMPLEMENTED LAYERS
=======================================================================

┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 1: SOURCE LAYER                                               │
│ Live SIH Portal (sih.gov.in) ──► Raw HTML Snapshot (sih2026_raw.html)│
└──────────────────────────────────┬──────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 2: NORMALIZATION & DATASET LAYER                              │
│ Cleaned JSON Dataset (data/sih2026_problem_statements.json)         │
│ Data Processors (scripts/vault_processor.py, verify_data.py)        │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 3: KNOWLEDGE & SPECIFICATION LAYER                            │
│ Problem Statements (01-Problem-Statements/*.md - 226 records)       │
│ Contracts & Metadata Specs (00-Meta/*.md)                           │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 4: NAVIGATION & INDEXING LAYER                                │
│ Theme Catalogs (02-Themes/)    │ Organization Catalogs (03-Orgs/)  │
│ Tech Catalogs (04-Tech/)       │ Domain Catalogs (05-Domains/)     │
│ Master Indices (06-Indexes/)   │ README.md & HOME.md Dashboard     │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 5: AGENT INTERFACE LAYER                                      │
│ Top-Level Entry (AGENTS.md)    │ Knowledge Rules (docs/AGENT-*)    │
└─────────────────────────────────────────────────────────────────────┘

=======================================================================
 PLANNED / FUTURE LAYERS (PHASE 3+)
=======================================================================

┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 6: DOWNSTREAM INTELLIGENCE & EXTENSIONS [PLANNED]            │
│ Vector Embeddings & RAG        │ Semantic Vector Search             │
│ Automated Feasibility Scoring  │ Team & Skill Matching Engines      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Layer Specifications

### Layer 1: Source Layer (CURRENT)
- **Components**: Live SIH Portal (`https://www.sih.gov.in/sih2026PS`), Raw local HTML snapshot (`data/sih2026_raw.html`).
- **Function**: Ground-truth evidence layer capturing official problem statements released for SIH 2026.

### Layer 2: Normalization & Dataset Layer (CURRENT)
- **Components**: `data/sih2026_problem_statements.json`, `scripts/vault_processor.py`, `scripts/verify_data.py`.
- **Function**: Standardizes text encoding (CP1252 to UTF-8), strips HTML markup, formats section breakdowns, extracts derived keyphrase metadata, and enforces dataset count integrity (226 records).

### Layer 3: Knowledge & Specification Layer (CURRENT)
- **Components**: `01-Problem-Statements/*.md`, `00-Meta/DATA-MODEL.md`, `PROVENANCE.md`, `TAXONOMY.md`, `GENERATION.md`, `VALIDATION.md`.
- **Function**: Rendered Markdown notes representing individual problem statements with YAML frontmatter, callout boxes, and relative links, governed by formal contracts.

### Layer 4: Navigation & Indexing Layer (CURRENT)
- **Components**: `02-Themes/`, `03-Organizations/`, `04-Technologies/`, `05-Domains/`, `06-Indexes/`, `README.md`, `HOME.md`.
- **Function**: Multi-dimensional catalog hubs enabling graph traversal and direct filtering by theme, nodal ministry, technology stack, sector domain, and project category.

### Layer 5: Agent Interface Layer (CURRENT)
- **Components**: `AGENTS.md`, `docs/AGENT-KNOWLEDGE-RULES.md`.
- **Function**: Guidance contract for AI agents detailing retrieval workflows, trust levels (`FACT`, `DERIVED`, `INFERENCE`, `RECOMMENDATION`), citation standards, and safe modification rules.

### Layer 6: Downstream Intelligence & Extensions (PLANNED - FUTURE PHASES)
- **Components**: RAG indexers, vector embeddings (`chromadb` / `qdrant`), semantic search endpoints, AI feasibility evaluators, team matching agents.
- **Function**: Higher-level reasoning applications consuming the vault knowledge base.
- **Status**: **PLANNED (Not implemented in Phase 2)**.

---

## 4. System Boundaries & Non-Goals

- **Data Layer Focus**: The vault is strictly a knowledge and data layer.
- **No Direct Embedding / RAG in Vault Core**: RAG databases and semantic embeddings belong to downstream consumers (Layer 6) and will not mutate the core Markdown/JSON vault.
- **Deterministic Maintenance**: All catalog pages and Markdown notes are deterministically generated from Layer 2.
