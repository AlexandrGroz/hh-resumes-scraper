from pathlib import Path
from typing import Iterable, Mapping

import pandas as pd


def build_dataframe(records: Iterable[Mapping[str, str]] | None) -> pd.DataFrame:
    if not records:
        return pd.DataFrame()

    return pd.DataFrame(list(records))


def save_dataframe(dataframe: pd.DataFrame, output_path: str) -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output, index=False)
