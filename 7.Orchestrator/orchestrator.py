import os
import subprocess
from pathlib import Path

from dagster import Definitions, job, op, In, Out, Config, Failure

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "1.Data_contract/olist_mini/contract.yaml"


def run(cmd: list[str], env: dict | None = None) -> None:
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    subprocess.run(cmd, cwd=str(ROOT), check=True, env=full_env)


class IngestionConfig(Config):
    run_ingestion: bool = True
    data_dir: str = "data/olist_mini"
    dataset: str = "raw_olist"


@op(out=Out(bool))
def check_contract_exists() -> bool:
    """Fail-fast if the data contract file does not exist."""
    if not CONTRACT.exists():
        raise Failure(f"Data contract not found at: {CONTRACT}")
    return True


@op(ins={"_dep": In(bool)}, out=Out(bool))
def validate_contract(_dep: bool) -> bool:
    run(["py", "2.Validation/contract_validator.py", str(CONTRACT)])
    return True


@op(ins={"_dep": In(bool)}, out=Out(bool))
def generate_ddl(_dep: bool) -> bool:
    # Use Data Contracts CLI to generate Databricks UC DDL
    run(["data-contract-cli", "ddl", "--dialect", "databricks", "--contract", str(CONTRACT), "--out", "4.DDL_for_catalogs/ddl_cli"]) 
    return True


@op(ins={"_dep": In(bool)}, out=Out(bool))
def generate_gx_suites(_dep: bool) -> bool:
    # Use Data Contracts CLI to generate GX suites
    run(["data-contract-cli", "gx", "--contract", str(CONTRACT), "--out", "5.GX_code/suites_cli"]) 
    return True


@op(ins={"_dep": In(bool)}, out=Out(Path))
def generate_dlt_pipeline(_dep: bool) -> Path:
    out_py = ROOT / "3.Ingestion/pipelines/contract_databricks_pipeline.py"
    run(["py", "3.Ingestion/generate_dlt_pipeline_databricks.py", str(CONTRACT)])
    return out_py


@op(ins={"pipe_path": In(Path)}, out=Out(bool))
def ingest(pipe_path: Path, cfg: IngestionConfig) -> bool:
    env = {
        "OLIST_DATA_DIR": cfg.data_dir,
        "DLT_DATASET": cfg.dataset,
        # require Databricks envs to be present in user environment
        # DATABRICKS_SERVER_HOSTNAME, DATABRICKS_HTTP_PATH, DATABRICKS_ACCESS_TOKEN
    }
    if cfg.run_ingestion:
        run(["py", str(pipe_path)], env=env)
    return True


@job
def build_and_ingest():
    c = check_contract_exists()
    v = validate_contract(c)
    d = generate_ddl(v)
    g = generate_gx_suites(d)
    p = generate_dlt_pipeline(g)
    ingest(p)


defs = Definitions(jobs=[build_and_ingest])
