# Great Expectations (GX) code generation

This step generates Great Expectations expectation suites from data contracts using the Data Contract CLI. These generated suites are then used by the DQ Transformation Framework in Step 6 for automated data quality validation.

## Purpose
- Generate GX expectation suites from data contracts using Data Contract CLI
- Store generated suites for use in Step 6 data processing
- Provide standardized data quality checks across the pipeline

## Prerequisites
- `datacontract-cli` installed (e.g., `pip install datacontract-cli`)
- Data contract from Step 1 validated and ready

## Quick Usage

### Using Shell Script (Linux/macOS/WSL)
```bash
# Generate suites from default contract
chmod +x generate-gx-suites.sh
./generate-gx-suites.sh

# Generate suites from specific contract
./generate-gx-suites.sh --contract ../../demo/contracts/my_contract.yaml --output ./my_suites
```

### Using PowerShell (Windows)
```powershell
# Generate suites from default contract
.\generate-gx-suites.ps1

# Generate suites from specific contract
.\generate-gx-suites.ps1 -Contract ..\..\demo\contracts\my_contract.yaml -Output .\my_suites
```

### Manual Generation
```bash
# Direct command (equivalent to scripts above)
datacontract export \
    --format great-expectations \
    --output ./suites_cli \
    ../../demo/contracts/contract.yaml
```

## Outputs
- **GX Expectation Suites**: JSON files under `./suites_cli/` containing Great Expectations suite definitions
- **Structured Organization**: Suites organized by table/dataset as defined in the data contract
- **Ready for Integration**: Suites are immediately usable by Step 6 DQ Transformation Framework

## Integration with Step 6

The generated GX suites are automatically used by the DQ Transformation Framework in Step 6:

1. **Default Configuration**: Step 6 automatically looks for suites in `../gx_generation/suites_cli/`
2. **Custom Path**: Configure Step 6 to use a different path via `data_quality.gx_config.suites_path`
3. **Fallback Generation**: If no pre-generated suites found, Step 6 will generate them on-the-fly

### Example Step 6 Configuration
```yaml
data_quality:
  gx_config:
    # Path to pre-generated GX suites from Step 5 (prioritized)
    suites_path: "../../gx_generation/suites_cli"
    
    # Path to data contract (fallback for generation)
    contract_path: "../../../demo/contracts/contract.yaml"
```

## Generated Suite Structure

```
suites_cli/
├── expectations/
│   ├── table1_suite.json          # Expectations for table1
│   ├── table2_suite.json          # Expectations for table2
│   └── ...
└── metadata/
    ├── suite_metadata.json        # Suite generation metadata
    └── contract_info.json          # Source contract information
```

## Benefits

✅ **Standardized Quality Checks**: Consistent DQ rules across all transformations  
✅ **Contract-Driven**: Quality checks automatically derived from data contract specifications  
✅ **Reusable**: Generated once, used by multiple transformations in Step 6  
✅ **Version Controlled**: GX suites can be committed and versioned with the codebase  
✅ **Performance**: Pre-generated suites eliminate generation overhead during transformations

## Workflow Integration

This step fits into the complete 6-step pipeline workflow:

1. **Data Contracts** → Define data structure and quality requirements
2. **Validation** → Validate contracts before proceeding  
3. **Ingestion** → Generate DLT scripts and ingest data
4. **DDL Generation** → Create schema definitions for target platforms
5. **GX Code Generation** → **THIS STEP** - Generate quality check suites
6. **Data Processing** → Execute transformations with enforced DQ checks using generated suites
7. **Orchestration** → Coordinate the complete pipeline

## Notes
- Generated suites can be customized after generation if needed
- Suites are automatically regenerated when contracts change
- Step 6 will fallback to dynamic generation if pre-generated suites are not found
- For complex quality requirements, consider extending contracts with custom expectations