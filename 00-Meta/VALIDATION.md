# Repository Validation Contract & Integrity Suite

> **SIH PS Vault 2026** · Data Integrity, Schema Validation & Verification Contract

---

## 1. Overview & Purpose

The **SIH PS Vault Validation Contract** establishes a strict, automated verification framework to ensure zero data loss, zero broken references, and 100% alignment between official source data, normalized JSON dataset, and generated Markdown artifacts.

All changes to the repository must be verified using the automated verification suite:
```bash
python3 scripts/verify_data.py
```

---

## 2. Validation Categories & Criteria

Validation is structured into six comprehensive categories:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. STRUCTURAL VALIDATION   (Record counts, ID ranges)       │
├─────────────────────────────────────────────────────────────┤
│ 2. SCHEMA VALIDATION       (JSON structure, YAML frontmatter)│
├─────────────────────────────────────────────────────────────┤
│ 3. CONSISTENCY VALIDATION  (Raw HTML ↔ JSON ↔ Markdown)     │
├─────────────────────────────────────────────────────────────┤
│ 4. RELATIONSHIP VALIDATION (Relative link integrity)         │
├─────────────────────────────────────────────────────────────┤
│ 5. PROVENANCE VALIDATION   (Official vs Derived separation)  │
├─────────────────────────────────────────────────────────────┤
│ 6. GENERATION VALIDATION   (Stale file check, reproducibility)│
└─────────────────────────────────────────────────────────────┘
```

### 2.1 Structural Validation

- **Checks**:
  - Total Problem Statement count equals exactly 226.
  - Problem Statement IDs are strictly continuous from `26001` to `26226` without gaps or duplicates.
  - All 226 Markdown PS files exist in `01-Problem-Statements/`.
- **Verdict Rules**:
  - **PASS**: Exactly 226 problems, IDs continuous `26001-26226`.
  - **FAIL**: Count != 226, missing/duplicate ID, or ID sequence gap.

### 2.2 Schema Validation

- **Checks**:
  - `data/sih2026_problem_statements.json` is valid UTF-8 JSON.
  - Every PS record contains required keys: `ps_id`, `title`, `organization`, `department`, `category`, `theme`, `description`.
  - Markdown note frontmatter contains valid YAML syntax.
- **Verdict Rules**:
  - **PASS**: Valid JSON & YAML schema compliance.
  - **FAIL**: Malformed JSON/YAML or missing required fields.

### 2.3 Consistency Validation

- **Checks**:
  - Field-by-field comparison between `data/sih2026_raw.html` (or live portal) and `data/sih2026_problem_statements.json` across `ps_id`, `title`, `description`, `organization`, `department`, `category`, `theme`.
  - Matching frontmatter `ps_id` and `title` between JSON dataset and rendered `PS-*.md` notes.
- **Verdict Rules**:
  - **PASS**: 100% field match after text normalization.
  - **FAIL**: Text mismatch, missing title/id, or content truncation.

### 2.4 Relationship & Link Integrity Validation

- **Checks**:
  - 100% scan of all internal Markdown relative links (matching label and relative path destination) across the entire repository.
  - Resolves target paths relative to source file directory.
  - Validates that target files exist on disk.
- **Verdict Rules**:
  - **PASS**: 0 broken relative links across all `.md` files.
  - **FAIL**: 1 or more broken relative links.

### 2.5 Provenance Validation

- **Checks**:
  - Verifies that derived fields (`technologies`, `domains`, `organization_type`, `has_dataset`, `aliases`) are stored in designated frontmatter blocks and tagged as derived.
  - Confirms official fields match raw source HTML text.
- **Verdict Rules**:
  - **PASS**: Clear separation between official and derived metadata.
  - **FAIL**: Official field modified without source justification or derived field labeled as official.

### 2.6 Generation & Stale Artifact Validation

- **Checks**:
  - Scans generated directories (`01-Problem-Statements/`, `02-Themes/`, `03-Organizations/`, `04-Technologies/`, `05-Domains/`, `06-Indexes/`) for orphaned or stale files not present in the expected manifest.
- **Verdict Rules**:
  - **PASS**: 0 orphaned or stale files.
  - **FAIL**: 1 or more orphaned files in generated directories.

---

## 3. Verification Report Specification

Running `python3 scripts/verify_data.py` executes all 6 validation phases and produces a machine-readable JSON artifact at `data/verification_report.json`:

```json
{
  "verification_timestamp": "2026-08-25T14:41:40",
  "source_url": "https://www.sih.gov.in/sih2026PS",
  "dataset_file": "data/sih2026_problem_statements.json",
  "total_problems": 226,
  "id_range": "26001-26226",
  "field_mismatches": {
    "ps_id": 0,
    "title": 0,
    "description": 0,
    "organization": 0,
    "department": 0,
    "category": 0,
    "theme": 0
  },
  "markdown_ps_count": 226,
  "broken_links_count": 0,
  "orphan_files_count": 0,
  "issues_count": 0,
  "warnings_count": 0,
  "verdict": "PASS"
}
```

---

## 4. Current Implemented vs. Planned Future Checks

| Check Type | Status | Tool |
| :--- | :---: | :--- |
| **226 PS Count & ID Range (26001-26226)** | **IMPLEMENTED** | `scripts/verify_data.py` |
| **Raw HTML ↔ JSON Field Comparison** | **IMPLEMENTED** | `scripts/verify_data.py` |
| **JSON ↔ Markdown Frontmatter Match** | **IMPLEMENTED** | `scripts/verify_data.py` |
| **Relative Markdown Link Scan** | **IMPLEMENTED** | `scripts/verify_data.py` |
| **Orphan/Stale Artifact Scan** | **IMPLEMENTED** | `scripts/verify_data.py` |
| **JSON Schema Validation (jsonschema)** | **PLANNED** | Future CI pipeline |
| **YAML Linting (yamllint)** | **PLANNED** | Future CI pipeline |
