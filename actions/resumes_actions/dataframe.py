from pathlib import Path
import pandas as pd
from typing import Iterable, Mapping


def build_dataframe(records: Iterable[Mapping[str, str]] | None) -> pd.DataFrame:
    if not records:
        return pd.DataFrame()

    return pd.DataFrame(list(records))


def save_dataframe(dataframe: pd.DataFrame, output_path: str) -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output, index=False)