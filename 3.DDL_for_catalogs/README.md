# 3. DDL for catalogs

Purpose
- Generate DDL to register datasets in data catalogs and/or the warehouse, based on contracts.

What goes here
- SQL DDL templates or generated files for your platform(s).
- Optional automation scripts to apply DDL.

Inputs
- Schemas/metadata from `../2.Validation/`.

Outputs
- DDL files (CREATE/ALTER) for tables, views, and metadata annotations.

Notes
- Keep platform-specific conventions isolated and reproducible.
