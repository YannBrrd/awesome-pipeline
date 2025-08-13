import os
import subprocess
from pathlib import Path

from dagster import Definitions, job, op, In, Out, Config

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
    destination: str = "duckdb"
    dataset: str = "raw_olist"


@op(out=Out(bool))
def validate_contract() -> bool:
    run(["py", "2.Validation/contract_validator.py", str(CONTRACT)])
    return True


@op(ins={"_dep": In(bool)}, out=Out(bool))
def generate_ddl(_dep: bool) -> bool:
    run(["py", "4.DDL_for_catalogs/generate_ddl.py"])
    return True


@op(ins={"_dep": In(bool)}, out=Out(bool))
def generate_gx_suites(_dep: bool) -> bool:
    run(["py", "5.GX_code/generate_gx_suites.py"])
    return True


@op(ins={"_dep": In(bool)}, out=Out(Path))
def generate_dlt_pipeline(_dep: bool) -> Path:
    out_py = ROOT / "3.Ingestion/pipelines/contract_pipeline.py"
    run(["py", "3.Ingestion/generate_dlt_pipeline.py", str(CONTRACT), str(out_py)])
    return out_py


@op(ins={"pipe_path": In(Path)}, out=Out(bool))
def ingest(pipe_path: Path, cfg: IngestionConfig) -> bool:
    env = {
        "OLIST_DATA_DIR": cfg.data_dir,
        "DLT_DESTINATION": cfg.destination,
        "DLT_DATASET": cfg.dataset,
    }
    if cfg.run_ingestion:
        run(["py", str(pipe_path)], env=env)
    return True


@job
def build_and_ingest():
    v = validate_contract()
    d = generate_ddl(v)
    g = generate_gx_suites(d)
    p = generate_dlt_pipeline(g)
    ingest(p)


defs = Definitions(jobs=[build_and_ingest])
