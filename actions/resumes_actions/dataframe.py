import re
from pathlib import Path
from typing import Iterable, Mapping, MutableSet

import pandas as pd


def build_dataframe(records: Iterable[Mapping[str, str]] | None) -> pd.DataFrame:
    if not records:
        return pd.DataFrame()

    return pd.DataFrame(list(records))


def save_dataframe(dataframe: pd.DataFrame, output_path: str) -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output, index=False)


def _slugify(value: str) -> str:
    slug = re.sub(r"[^\w]+", "_", value.strip().lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "all"


def query_output_path(base_path: str, query: str) -> Path:
    output = Path(base_path)
    slug = _slugify(query)
    return output.with_name(f"{output.stem}_{slug}{output.suffix}")


def load_existing_ids(path: str) -> MutableSet[str]:
    output = Path(path)
    if not output.exists():
        return set()

    try:
        dataframe = pd.read_csv(output)
    except pd.errors.EmptyDataError:
        return set()

    if "resume_id" not in dataframe.columns:
        return set()

    ids = dataframe["resume_id"].dropna().astype(str)
    return set(ids)


def append_record(record: Mapping[str, str], *, path: str, known_ids: MutableSet[str]) -> bool:
    resume_id = str(record.get("resume_id", "")).strip()
    if resume_id and resume_id in known_ids:
        return False

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)

    dataframe = pd.DataFrame([record])
    write_header = not output.exists()
    dataframe.to_csv(output, mode="a", header=write_header, index=False)

    if resume_id:
        known_ids.add(resume_id)

    return True
