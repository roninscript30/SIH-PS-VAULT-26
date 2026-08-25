# AGENTS.md

## SIH PS Vault — Agent Instructions

This repository is the **SIH PS Vault**, a structured knowledge base containing
the Smart India Hackathon (SIH) 2026 problem statements and their associated
metadata, classifications, relationships, indexes, and machine-readable data.

The repository is designed to be usable by:

- Humans through Obsidian and Markdown
- Scripts and data-processing tools
- AI/coding agents
- Future search, RAG, evaluation, and other downstream systems

The vault is primarily a **knowledge and data layer**.

It is not itself the evaluation, ranking, RAG, or solution-generation system.

---

# Knowledge Contracts & Reference Documentation

Agents operating on this repository must reference the formal knowledge contracts and technical specifications:

| Contract / Specification | File Path | Focus Area |
| :--- | :--- | :--- |
| 📊 **Canonical Data Model** | [`00-Meta/DATA-MODEL.md`](00-Meta/DATA-MODEL.md) | PS Entity, Field Ownership Table, Relationship Semantics |
| 🏛️ **Data Provenance Standard** | [`00-Meta/PROVENANCE.md`](00-Meta/PROVENANCE.md) | 5-Tier Authority, Snapshot vs Live Rules, Conflict Resolution |
| 🏷️ **Taxonomy Specifications** | [`00-Meta/TAXONOMY.md`](00-Meta/TAXONOMY.md) | Official vs Derived Taxonomies, Regex Classifier Specs |
| 🔄 **Generation Pipeline Specification** | [`00-Meta/GENERATION.md`](00-Meta/GENERATION.md) | Build Pipeline, Path Classifications, Stale Artifact Cleanup |
| 🧪 **Validation Contract** | [`00-Meta/VALIDATION.md`](00-Meta/VALIDATION.md) | Verification Criteria, PASS/FAIL Rules, Audit Report Schema |
| 🤖 **Agent Knowledge Rules** | [`docs/AGENT-KNOWLEDGE-RULES.md`](docs/AGENT-KNOWLEDGE-RULES.md) | Retrieval Hierarchy, FACT vs INFERENCE Rules, Citation |
| 🏗️ **System Architecture** | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | 6-Layer Architectural Model (Current vs Planned) |

---

# 1. Core Principle

Treat this repository as a knowledge base, not as an ordinary collection of
Markdown documents.

Agents must preserve the distinction between:

1. Official source information
2. Derived information
3. Generated artifacts
4. Agent analysis and inference

Never present derived or inferred information as official SIH information.

---

# 2. Knowledge Model

The core entity is a Problem Statement (PS).

A problem statement may be associated with:

- Theme
- Organization
- Department / Ministry
- Category
- Technology
- Domain
- Source
- Related problem statements

Conceptually:

    Problem Statement
        ├── belongs to → Theme
        ├── issued by → Organization
        ├── classified as → Category
        ├── classified into → Domain
        ├── associated with → Technology
        └── sourced from → SIH

Not every relationship has the same level of authority.

---

# 3. Information Provenance

Information must be treated according to its provenance.

## Official

Information directly originating from the SIH source should be treated as
official source information.

Examples include:

- Problem Statement ID
- Problem Statement title
- Organization
- Department / Ministry
- Category
- Theme
- Original problem statement content
- Official source references

## Derived

Information inferred or classified by repository tooling is derived data.

Examples may include:

- Technologies
- Domains
- Organization type
- Dataset indicators
- Keyword classifications
- Similarity relationships

Derived information must not be described as official SIH metadata.

## Generated

Some repository files are generated from the underlying dataset.

Examples include:

- Indexes
- Taxonomy pages
- Cross-reference pages
- Export files
- Other generated representations

Generated files should not be manually edited unless explicitly documented as
manual content.

## Analysis / Inference

Reasoning produced by an agent or human is not part of the official source.

Examples:

- Feasibility assessment
- Architecture proposals
- Ranking
- Recommendations
- Team-fit analysis
- Solution ideas

Keep analysis separate from the core source problem statement whenever
possible.

---

# 4. Source of Truth

Use the following conceptual hierarchy:

    Official SIH source
            ↓
    Raw source snapshot
            ↓
    Normalized dataset
            ↓
    Vault representations
            ↓
    Indexes / exports / downstream systems

The local raw source snapshot is evidence of the source at a particular point
in time. It should not automatically be treated as permanently authoritative
over the live SIH source.

When sources disagree:

1. Do not silently overwrite information.
2. Identify the conflicting sources.
3. Determine whether the difference is caused by formatting, extraction,
   normalization, or an actual source change.
4. Preserve provenance.
5. Document unresolved uncertainty.

Never invent missing source information.

---

# 5. Repository Structure

The major repository areas are:

    00-Meta/
        Repository documentation and metadata rules

    01-Problem-Statements/
        Individual SIH problem statement records

    02-Themes/
        Theme-based navigation and relationships

    03-Organizations/
        Organization-based navigation and relationships

    04-Technologies/
        Technology classifications and navigation

    05-Domains/
        Domain classifications and navigation

    06-Indexes/
        Generated indexes and lookup structures

    data/
        Machine-readable and source data

    scripts/
        Data processing, generation, and validation tooling

    .obsidian/
        Obsidian vault configuration

Read the relevant metadata/documentation before making structural changes.

---

# 6. Problem Statement Retrieval

When answering questions about problem statements:

1. Identify the PS ID if one is provided.
2. Otherwise search using the most specific available metadata.
3. Retrieve the actual problem statement record.
4. Inspect its metadata and content.
5. Use related taxonomy/index files when useful.
6. Distinguish official metadata from derived classifications.
7. Base factual claims on the source record.

Do not infer the contents of a problem statement from its filename, folder,
theme, technology, or title alone.

For comparisons, retrieve the complete relevant records before comparing them.

---

# 7. Search Strategy

Prefer structured retrieval before broad text scanning.

For example:

    PS ID
       ↓
    Problem Statement
       ↓
    Metadata
       ↓
    Taxonomy / Index
       ↓
    Related records

Use indexes and taxonomy pages for discovery.

Use the individual PS record as the primary source for the actual problem
statement content.

Do not treat an index entry as a replacement for the underlying PS record.

---

# 8. Reasoning Rules

Agents must clearly separate:

### Fact

Directly supported by repository/source data.

### Derived fact

Produced by deterministic repository classification or processing.

### Inference

Reasoned from available information but not directly stated by the source.

### Recommendation

A proposed action or decision based on analysis.

When useful, explicitly state which category a conclusion belongs to.

Example:

    FACT:
    The problem statement belongs to the Software category.

    DERIVED:
    The repository classifies it under Computer Vision.

    INFERENCE:
    The problem may require image-processing capabilities.

    RECOMMENDATION:
    A computer-vision-based architecture could be evaluated.

Do not collapse these categories into one statement.

---

# 9. Modification Rules

Agents may modify repository files only when explicitly instructed.

Before modifying data:

1. Understand the generation pipeline.
2. Determine whether the target file is source or generated.
3. Prefer fixing the source/generation process instead of manually editing
   generated output.
4. Preserve existing PS IDs.
5. Avoid accidental content loss.
6. Run validation after modifications.

Never manually edit hundreds of generated records when the underlying
generator can be corrected instead.

---

# 10. Problem Statement Integrity

Problem statement records are high-value source data.

Agents must not:

- Invent missing descriptions
- Rewrite official problem statements
- Change official metadata without evidence
- Change PS IDs
- Merge different PS records
- Delete PS records without explicit instruction
- Treat AI-generated summaries as official content

Formatting normalization is allowed only when it does not alter the meaning
or source content.

---

# 11. Generated Artifacts

Before modifying an index, taxonomy page, export, or other generated artifact:

Determine whether it can be regenerated from source data.

If it can:

    Fix source/generator
          ↓
    Regenerate artifact
          ↓
    Validate result

Do not manually patch generated output when doing so would create a
source-of-truth conflict.

---

# 12. Validation

After data or generation changes, validate at minimum:

- Problem statement count
- Unique PS IDs
- Required metadata
- YAML validity
- JSON validity
- Markdown/JSON consistency
- Internal links
- Taxonomy references
- Generated indexes
- Duplicate records
- Source references

A change is not considered complete merely because the modified file looks
correct.

Run the repository's available validation tooling.

If validation fails, report the failure rather than hiding or bypassing it.

---

# 13. Agent Safety

When uncertain:

- Inspect before modifying.
- Prefer evidence over assumptions.
- Preserve source information.
- Avoid destructive operations.
- Do not silently resolve conflicting data.
- Do not claim verification that has not been performed.
- Do not add new classifications without identifying them as derived.
- Do not modify unrelated files.

For large-scale changes:

    Inspect
      ↓
    Explain
      ↓
    Modify
      ↓
    Validate
      ↓
    Report

---

# 14. Downstream Systems

This vault may later be consumed by:

- Search systems
- RAG systems
- AI agents
- Evaluation engines
- Ranking systems
- Recommendation systems
- Web applications
- APIs
- Data-analysis pipelines

These systems should consume the knowledge base rather than embedding their
own conflicting copies of the source data.

Downstream analysis should remain distinguishable from the source knowledge.

---

# 15. Documentation

Before making significant architectural changes, inspect the documentation
under `00-Meta/` and `docs/` if present.

Important documentation should eventually cover:

- Data model
- Provenance
- Taxonomy
- Generation pipeline
- Validation
- Agent workflows
- Architecture

Keep this file focused on agent orientation and repository-wide rules.
Detailed specifications belong in dedicated documentation.

---

# 16. Agent Task Completion

When completing a repository task, report:

1. What was changed
2. Why it was changed
3. Which source/generator was modified
4. Which generated artifacts were regenerated
5. What validation was performed
6. Any remaining warnings or uncertainties

Never claim a task is fully validated unless the relevant validation actually
passed.

---

# 17. Guiding Principle

The SIH PS Vault should remain:

    Trustworthy
    Structured
    Reproducible
    Traceable
    Human-readable
    Machine-readable
    Agent-readable

The goal is not to make the vault contain every possible analysis.

The goal is to make the vault a reliable knowledge layer from which humans,
agents, and downstream systems can reason.