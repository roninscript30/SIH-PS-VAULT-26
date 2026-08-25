# Repository Taxonomy Specification & Classification Rules

> **SIH PS Vault 2026** · Taxonomies, Classification Systems & Known Limitations

---

## 1. Executive Summary

The **SIH PS Vault** utilizes five distinct classification systems (taxonomies) to organize and cross-link problem statements. 

These taxonomies are strictly divided by authority:
- **Official SIH Taxonomies**: Categories, Themes, and Nodal Organizations.
- **Derived Vault Taxonomies**: Technologies and Sector Domains.

---

## 2. Taxonomy Specifications

### 2.1 Category Taxonomy (Official)

- **Definition**: The fundamental operational track assigned to a problem statement.
- **Values**:
  - `Software`: 172 problems (Web, Mobile, AI/ML, Cloud, GIS, Data platforms).
  - `Hardware`: 54 problems (Embedded systems, Robotics, Drones, IoT, Sensors, physical prototypes).
- **Source**: Official SIH 2026 Portal.
- **Authority**: **Official Ground Truth**.
- **Assignment Logic**: Direct extraction from official modal field `Category`.
- **Storage Location**: `category` field in `sih2026_problem_statements.json` and YAML frontmatter.
- **Catalog Location**: `06-Indexes/category_index.md`.
- **Known Limitations**: Categorization is fixed by SIH organizers; some software problems may contain hardware edge components or vice versa.

---

### 2.2 Theme Taxonomy (Official)

- **Definition**: The primary problem domain category designated by SIH organizers.
- **Values**: 18 official themes (e.g. `Smart Automation`, `MedTech / BioTech / HealthTech`, `Disaster Management`, `Agriculture, FoodTech & Rural Development`, `Space Technology`).
- **Source**: Official SIH 2026 Portal.
- **Authority**: **Official Ground Truth**.
- **Assignment Logic**: Direct extraction from official modal field `Theme`.
- **Storage Location**: `theme` field in `sih2026_problem_statements.json` and YAML frontmatter.
- **Catalog Location**: `02-Themes/theme_index.md` + 18 individual theme catalog files in `02-Themes/*.md`.
- **Known Limitations**: Every problem statement is assigned to exactly one theme by SIH organizers, even if cross-disciplinary.

---

### 2.3 Organization Taxonomy (Official)

- **Definition**: The nodal entity issuing the problem statement.
- **Values**: 30 distinct organizations (e.g. `Ministry of Railways`, `ISRO`, `DRDO`, `Ministry of Defence`, `AICTE`).
- **Source**: Official SIH 2026 Portal.
- **Authority**: **Official Ground Truth**.
- **Assignment Logic**: Direct extraction from official modal field `Organization`.
- **Storage Location**: `organization` and `department` fields in JSON dataset and YAML frontmatter.
- **Catalog Location**: `03-Organizations/organization_index.md` + 30 individual organization hub files in `03-Organizations/*.md`.
- **Known Limitations**: Name variations in raw data (e.g. `"Governmcnt"` vs `"Government"`) are normalized during dataset processing.

---

### 2.4 Technology Taxonomy (Derived)

- **Definition**: Technical concept tags representing required or suggested technologies.
- **Values**: 20 normalized technology tags (`AI-and-ML`, `Computer-Vision`, `NLP`, `IoT-and-Sensors`, `Blockchain`, `GIS-and-Geospatial`, `Robotics`, `Cloud-Computing`, `Mobile-Development`, `Web-Platforms`, `Data-Analytics`, `Cybersecurity-Tech`, `AR-VR`, `Digital-Twin`, `Edge-Computing`, `LiDAR`, `Quantum-Computing`, `GPS-and-Navigation`, `3D-Modeling`, `Sonar-Acoustics`).
- **Source**: Repository Keyphrase Regex Classifier (`scripts/vault_config.TECH_KEYWORDS`).
- **Authority**: **Derived Metadata** (Vault Enriched).
- **Assignment Logic**: Case-insensitive regex matching over `title + description`.
- **Storage Location**: `_technologies` in memory / `technologies` list in YAML frontmatter.
- **Catalog Location**: `04-Technologies/technology_index.md` + 20 technology catalog files in `04-Technologies/*.md`.
- **Known Limitations**: See Section 3 below.

---

### 2.5 Domain Taxonomy (Derived)

- **Definition**: Industry sector or functional domain classification.
- **Values**: 17 normalized domain tags (`Healthcare`, `Agriculture`, `Mining`, `Defence-and-Military`, `Land-Management`, `Weather-and-Climate`, `Ocean-and-Marine`, `Transportation`, `Education-and-Skilling`, `Disaster-Response`, `Law-Enforcement`, `Energy-and-Petroleum`, `Urban-Development`, `E-Governance`, `Space-Exploration`, `Social-Welfare`).
- **Source**: Repository Keyphrase Regex Classifier (`scripts/vault_config.DOMAIN_KEYWORDS`).
- **Authority**: **Derived Metadata** (Vault Enriched).
- **Assignment Logic**: Case-insensitive regex matching over `title + description`.
- **Storage Location**: `_domains` in memory / `domains` list in YAML frontmatter.
- **Catalog Location**: `05-Domains/domain_index.md` + 17 domain classification files in `05-Domains/*.md`.
- **Known Limitations**: See Section 3 below.

---

## 3. Important Notice on Derived Taxonomies (Technologies & Domains)

> [!WARNING]
> **DERIVED TAXONOMY LIMITATIONS**
> 
> 1. **Not Official Metadata**: Technology and Domain tags are **NOT** provided by the official SIH 2026 portal. They are computed by repository tools.
> 2. **Rule-Based Matching**: Classifications are derived using regular expressions defined in `scripts/vault_config.py`.
> 3. **False Positives**: Keyword matches (e.g. matching `"train"` in `"training model"`) can occasionally tag a problem with an unintended technology or domain.
> 4. **False Negatives**: If a problem description uses non-standard terminology not covered in regex patterns, tags may be missed.
> 5. **Discovery Aids Only**: Derived tags exist purely as discovery aids for filtering and graph exploration. Agents and researchers must read the underlying official problem text for authoritative technical scope.
