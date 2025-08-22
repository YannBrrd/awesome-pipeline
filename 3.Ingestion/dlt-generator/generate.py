import argparse
import os
from pathlib import Path
from typing import Any, Dict, List

import yaml
import questionary
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import ValidationError

from contract_model import Contract

def load_yaml(path: Path) -> Dict[str, Any]:
    """Charge un fichier YAML et retourne son contenu."""
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def dump_yaml(data: Dict[str, Any], path: Path) -> None:
    """Sauvegarde des données dans un fichier YAML."""
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

def ensure_out_dir(out_dir: Path) -> None:
    """Crée le répertoire de sortie s'il n'existe pas."""
    out_dir.mkdir(parents=True, exist_ok=True)

def jinja_env() -> Environment:
    """Configure l'environnement Jinja2 pour le rendu des templates."""
    return Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(disabled_extensions=("j2",)),
        trim_blocks=True,
        lstrip_blocks=True,
    )

def set_in(d: Dict[str, Any], loc: List[str], value: Any) -> None:
    """Définit une valeur dans un dictionnaire imbriqué via un chemin."""
    cur = d
    for k in loc[:-1]:
        if isinstance(k, int):
            raise ValueError("Index lists non supportés ici")
        cur = cur.setdefault(k, {})
    cur[loc[-1]] = value

def ask_for_value(path: List[str], msg: str, choices: List[str] | None = None) -> Any:
    """Demande une valeur à l'utilisateur via Questionary."""
    dotted = ".".join(path)
    if choices:
        return questionary.select(f"{msg} ({dotted})", choices=choices).ask()
    return questionary.text(f"{msg} ({dotted})").ask()

def ask_missing(contract_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Demande interactivement les champs manquants jusqu'à validation complète."""
    while True:
        try:
            Contract.model_validate(contract_dict)
            return contract_dict
        except ValidationError as e:
            for err in e.errors():
                loc = list(err["loc"])
                msg = err["msg"]
                # Heuristiques de prompts selon le chemin
                if loc == ["pipeline", "name"]:
                    val = ask_for_value(loc, "Nom du pipeline")
                    set_in(contract_dict, loc, val)
                elif loc == ["source", "base_url"]:
                    val = ask_for_value(loc, "URL de base de l'API (https://...)")
                    set_in(contract_dict, loc, val)
                elif loc == ["source", "auth", "kind"]:
                    val = ask_for_value(loc, "Type d'authentification", ["none", "bearer_token", "basic"])
                    set_in(contract_dict, loc, val)
                elif loc == ["source", "auth", "token_env"]:
                    val = ask_for_value(loc, "Nom de la variable d'env pour le token (ex: API_TOKEN)")
                    set_in(contract_dict, loc, val)
                elif loc == ["source", "auth", "username"]:
                    val = ask_for_value(loc, "Nom d'utilisateur pour auth basic")
                    set_in(contract_dict, loc, val)
                elif loc == ["source", "auth", "password_env"]:
                    val = ask_for_value(loc, "Nom de la variable d'env pour le mot de passe basic")
                    set_in(contract_dict, loc, val)
                elif loc == ["destination", "type"]:
                    val = ask_for_value(loc, "Destination", ["duckdb", "postgres", "bigquery", "snowflake", "databricks"])
                    set_in(contract_dict, loc, val)
                elif loc == ["destination", "dataset"]:
                    val = ask_for_value(loc, "Dataset (BigQuery)")
                    set_in(contract_dict, loc, val)
                elif loc == ["destination", "schema"]:
                    val = ask_for_value(loc, "Schéma (Postgres/DuckDB/Snowflake/Databricks)")
                    set_in(contract_dict, loc, val)
                elif loc == ["destination", "merge_key"]:
                    val = ask_for_value(loc, "Clé(s) de merge (séparées par des virgules)")
                    set_in(contract_dict, loc, [k.strip() for k in val.split(",") if k.strip()])
                else:
                    # Fallback générique
                    val = ask_for_value([str(x) for x in loc], f"{msg}. Saisir une valeur")
                    set_in(contract_dict, loc, val)

def render_templates(contract: Contract, out_dir: Path) -> None:
    """Génère les fichiers de sortie à partir des templates Jinja2."""
    env = jinja_env()
    ctx = {"c": contract.model_dump()}
    for name in ["ingest.py.j2", "README.md.j2", "env.example.j2"]:
        tpl = env.get_template(name)
        rendered = tpl.render(**ctx)
        target = out_dir / name.replace(".j2", "")
        target.write_text(rendered, encoding="utf-8")
    # Recopier le contrat complété pour exécution runtime
    dump_yaml(contract.model_dump(), out_dir / "contract.yaml")

def main() -> None:
    """Point d'entrée principal du CLI."""
    parser = argparse.ArgumentParser(description="Génère un script dlt à partir d'un data contract")
    parser.add_argument("--contract", required=True, help="Chemin vers contract.yaml")
    parser.add_argument("--out", default="build", help="Répertoire de sortie")
    args = parser.parse_args()

    contract_path = Path(args.contract)
    out_dir = Path(args.out)
    ensure_out_dir(out_dir)

    # Charger YAML existant
    raw = load_yaml(contract_path)
    if not raw:
        print("contract.yaml vide ou introuvable.")
        raise SystemExit(1)

    # Demander les champs manquants/invalides
    completed = ask_missing(raw)

    # Valider final et réécrire le contrat d'entrée
    model = Contract.model_validate(completed)
    dump_yaml(model.model_dump(), contract_path)

    # Générer les fichiers
    render_templates(model, out_dir)

    print(f"OK. Fichiers générés dans: {out_dir.resolve()}")
    print("- ingest.py")
    print("- README.md")
    print("- .env.example")
    print("- contract.yaml (copie du contrat complété)")

if __name__ == "__main__":
    main()
