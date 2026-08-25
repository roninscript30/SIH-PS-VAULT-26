# AI Agent Knowledge Interpretation & Governance Rules

> **SIH PS Vault 2026** · Operational Rules for AI Agents, LLM Pipelines & Automated Tooling

---

## 1. Overview & Purpose

This document defines the **Knowledge Contract** for AI coding assistants, downstream agents, RAG systems, and evaluation pipelines interacting with the **SIH PS Vault**.

Agents operating on this repository must adhere to strict principles of data provenance, evidence-based reasoning, and non-destructive modification.

---

## 2. Structured Retrieval Strategy

When querying or analyzing the vault, agents must follow a structured retrieval order:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Individual PS Notes (01-Problem-Statements/PS-*.md)      │
│    └─ Primary source for complete problem content & text.   │
├─────────────────────────────────────────────────────────────┤
│ 2. Canonical JSON Dataset (data/sih2026_problem_statements) │
│    └─ Primary source for programmatic filtering & scripts.  │
├─────────────────────────────────────────────────────────────┤
│ 3. Taxonomies & Indexes (02-Themes/, 04-Technologies/, etc.) │
│    └─ Primary source for discovery & navigation.            │
├─────────────────────────────────────────────────────────────┤
│ 4. Raw Source HTML (data/sih2026_raw.html)                  │
│    └─ Ultimate verification snapshot for text audit.        │
└─────────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **No Inferred Summaries**: Do not infer problem statement content or technical scope from filenames, folder names, theme titles, or index entries alone. Always retrieve the underlying PS record before answering user questions.

---

## 3. Trust & Statement Classification Rules

Agents must explicitly categorize claims in their reasoning or output into four distinct levels:

### 3.1 FACT
Directly supported by official portal data (`ps_id`, `title`, `organization`, `department`, `category`, `theme`, official description).
> *Example*: `"FACT: PS 26001 is issued by the Ministry of Health and Family Welfare under the Hardware category."`

### 3.2 DERIVED FACT
Produced by deterministic repository classification tooling (technology keyphrase matching, domain tagger, org classifier).
> *Example*: `"DERIVED: The repository classifies PS 26001 under AI-and-ML and Computer-Vision."`

### 3.3 INFERENCE
Reasoned by the agent or model from available information, but not explicitly stated by official sources.
> *Example*: `"INFERENCE: This problem likely requires an edge computing module for real-time inference on low-power devices."`

### 3.4 RECOMMENDATION
A proposed action, technical choice, team alignment, or solution architecture suggested by the agent.
> *Example*: `"RECOMMENDATION: A PyTorch-based vision pipeline targeting mobile devices could be evaluated for this challenge."`

**Rule**: Agents must **NEVER** collapse these categories into a single statement presenting inferences or recommendations as official SIH facts.

---

## 4. Evidence & Citation Protocol

- When answering queries about problem statements, agents must cite the exact `ps_id` (e.g., `PS 26001`).
- When making claims about dataset properties or source metadata, agents should reference the canonical JSON dataset (`data/sih2026_problem_statements.json`).
- If derived technology tags are referenced, agents must state that they are derived analytics provided by the vault classifier.

---

## 5. Handling Uncertainty & Conflicts

- **No Overwriting Uncertainty**: If an agent discovers a conflict between sources (e.g. live portal vs. snapshot), the agent must report the conflict clearly rather than picking one silently.
- **No Content Fabrication**: Agents must **never** invent missing background descriptions, fabricate dataset links, or guess missing fields.

---

## 6. Repository Modification Rules

When instructed to modify or maintain repository data, agents must follow these strict guidelines:

1. **Never Patch Generated Output**: Do not manually edit rendered Markdown notes in `01-Problem-Statements/`, `02-Themes/`, `03-Organizations/`, `04-Technologies/`, `05-Domains/`, or `06-Indexes/`.
2. **Fix Source or Generator First**:
   - If a derived tag is incorrect: update regex rules in `scripts/vault_config.py`.
   - If render layout needs updating: modify template in `scripts/vault_generators.py`.
   - If raw text needs fixing: update `data/sih2026_problem_statements.json` after verifying against `data/sih2026_raw.html`.
3. **Regenerate and Validate**:
   - Run `python3 scripts/generate_vault.py` to rebuild generated files.
   - Run `python3 scripts/verify_data.py` to validate link integrity and dataset consistency.
   - Never claim validation passed unless `verify_data.py` explicitly returned a `PASS` verdict.
