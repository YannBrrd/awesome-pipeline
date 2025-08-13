# 1. Data contract

Purpose
- Define producer-owned, versioned data contracts that drive the rest of the pipeline.

What goes here
- Contract definitions (YAML/JSON), one per dataset/domain.
- Optional examples and sample payloads for producers/consumers.

Suggested layout
- contracts/<domain>/<dataset>/contract.yaml
- contracts/<domain>/<dataset>/README.md
- contracts/<domain>/<dataset>/samples/*.json

Minimum sections to capture
- metadata: name, owner, domain, description, contacts
- lifecycle: version, release date, change log
- distribution: refresh cadence, channel, SLAs
- schema: fields, types, nullability, keys, constraints
- quality: rules/tolerances (nulls, uniqueness, ranges)
- privacy/security: PII flags, classification, retention

Flow
1) Author/review contract. 2) Validate and compile in `../2.Validation/`. 3) Outputs feed `../3.Ingestion/`, `../4.DDL_for_catalogs/`, `../5.GX_code/`, and `../6.Data_processing/`.
