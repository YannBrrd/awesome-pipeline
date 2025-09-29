from typing import Dict, List, Optional, Literal, Any
from pydantic import BaseModel, Field, HttpUrl, field_validator

class Auth(BaseModel):
    kind: Literal["none", "bearer_token", "basic"] = "none"
    token_env: Optional[str] = None
    username: Optional[str] = None
    password_env: Optional[str] = None

    @field_validator("token_env")
    @classmethod
    def need_token_if_bearer(cls, v, info):
        if info.data.get("kind") == "bearer_token" and not v:
            raise ValueError("token_env requis si auth.kind=bearer_token")
        return v

    @field_validator("username", "password_env")
    @classmethod
    def need_basic_if_basic(cls, v, info):
        if info.data.get("kind") == "basic" and not v:
            raise ValueError(f"{info.field_name} requis si auth.kind=basic")
        return v

class Pagination(BaseModel):
    type: Literal["none", "page"] = "none"
    page_param: Optional[str] = None
    start: int = 1
    limit_param: Optional[str] = None
    page_size: Optional[int] = None

class Incremental(BaseModel):
    mode: Literal["none", "cursor", "full_refresh"] = "none"
    cursor_field: Optional[str] = None
    start_value: Optional[str] = None
    pagination: Pagination = Pagination()

class SourceAPI(BaseModel):
    type: Literal["api"] = "api"
    base_url: HttpUrl
    auth: Auth = Auth()
    incremental: Incremental = Incremental()
    items_path: Optional[str] = None  # chemin JSON (dot/brackets) vers la liste

class Destination(BaseModel):
    type: Literal["duckdb", "postgres", "bigquery", "snowflake", "databricks"]
    dataset: Optional[str] = None  # pour BigQuery
    schema: Optional[str] = None   # pour Postgres/DuckDB/Snowflake/Databricks
    write_disposition: Literal["append", "replace", "merge"] = "append"
    merge_key: Optional[List[str]] = None

    @field_validator("dataset")
    @classmethod
    def dataset_if_bq(cls, v, info):
        if info.data.get("type") == "bigquery" and not v:
            raise ValueError("destination.dataset requis pour BigQuery")
        return v

    @field_validator("schema")
    @classmethod
    def schema_if_not_bq(cls, v, info):
        if info.data.get("type") in ("postgres", "duckdb", "snowflake", "databricks") and not v:
            raise ValueError("destination.schema requis pour Postgres/DuckDB/Snowflake/Databricks")
        return v

    @field_validator("merge_key")
    @classmethod
    def merge_needs_key(cls, v, info):
        if info.data.get("write_disposition") == "merge" and not v:
            raise ValueError("destination.merge_key requis si write_disposition=merge")
        return v

class Column(BaseModel):
    type: Literal["bigint", "int", "text", "decimal", "timestamp", "boolean", "json"]
    nullable: bool = True
    in_set: Optional[List[str]] = None
    min: Optional[float] = None
    max: Optional[float] = None
    precision: Optional[int] = None
    scale: Optional[int] = None

class Resource(BaseModel):
    primary_key: List[str] = Field(default_factory=list)
    columns: Dict[str, Column]

class Pipeline(BaseModel):
    name: str

class Contract(BaseModel):
    version: str = "1.0"
    pipeline: Pipeline
    source: SourceAPI
    destination: Destination
    schema: Dict[str, Resource]
