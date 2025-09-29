We are working on a data pipeline framework based on data contracts. This framework aims to standardize data exchange between different components of the system, ensuring data integrity and consistency throughout the pipeline.

Generated framework should be generic, and allowing multiple data sources and sinks to be easily integrated into the pipeline including major players like BigQuery, Databricks, Snowflake and MS Fabric. DuckDB will be used as a testing platform, so include it.

Sourcing is done through DLTHub. We should inject 'expects' in DLT script when generating using Pydantic.

Data quality checks will be based on Great Expectations (GX). The framework should provide built-in support for defining and running these checks as part of the data pipeline.

Data contract will be validated using Data Contract CLI.

GX code should be also generated using Data Contract CLI.

All scripts should be cross platform shell scripts.

The target is not to generate the pipeline here, but create the tools to generate the pipeline.

In the end, we want to provide a seamless experience for data engineers to define, validate, and execute their data pipelines with minimal friction, including DQ rules and full lineage.

We'll also provide an example of the execution, based on CSV and duckDB + a data catalog.

Every comment including readme and stuff should always be in english.

Workflow will be 
1. Provide your data contract
2. Validate using Data Contract CLI
3. Generate DLT script using Pydantic
4. Generate DDL for data catalogs using Data Contract CLI
5. Generate GX code to integrate data quality checks into the pipeline.
6. Execute the pipeline