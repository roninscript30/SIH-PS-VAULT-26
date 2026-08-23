---
type: meta
---
# ℹ️ About This Vault

## Data Source
- **URL**: [https://www.sih.gov.in/sih2026PS](https://www.sih.gov.in/sih2026PS)
- **Scraped**: Automated extraction from HTML modals
- **Verified**: Independent re-parse + field-by-field comparison against live site

## Methodology
1. All 226 problem statement modals scraped from official SIH 2026 portal
2. CP1252→UTF-8 encoding artifacts repaired (curly quotes, degree symbols, etc.)
3. Independent verification confirmed 0 data loss, 0 missing problems, 0 truncation
4. Technologies and domains auto-extracted via keyword matching
5. Evaluation scores generated via content-based heuristics (clearly marked as estimates)
6. Similarity detection via org/theme/tech/domain overlap analysis

## Key Distinction
- **🔵 Official Facts**: Direct from SIH portal (Layer 1, frontmatter)
- **🟡 Derived Analysis**: Auto-extracted classifications (Layer 3, technologies/domains)
- **🔴 Analytical Estimates**: Scores and strategic groupings (Layers 7-8)

## Vault Structure
- `01-Problem-Statements/` — 226 PS files with 9 knowledge layers each
- `02-Themes/` — 18 theme hub pages
- `03-Organizations/` — 30 organization pages
- `04-Technologies/` — Technology concept nodes
- `05-Domains/` — Domain classification pages
- `06-Analysis/` — Evaluation, similarity, shortlist, innovation analysis
- `07-Indexes/` — Master tables and filtered views
