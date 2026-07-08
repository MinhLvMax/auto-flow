import pandas as pd
from typing import Any, List
from src.auto_prompt.models.script_row import ScriptRow
from .base import ScriptParser

class ScriptColumn:
    INDEX = "Unnamed: 0"
    SCRIPT = "KỊCH BẢN"
    TRANSLATION = "DỊCH"
    CHARACTER_COUNT = "KÝ TỰ"
    TOTAL = "TỔNG"

class ExcelScriptParser(ScriptParser):

    def parse(self, raw: Any) -> List[ScriptRow]:
        """
        raw = path to .xlsx file
        """

        df = pd.read_excel(raw)

        rows: List[ScriptRow] = []

        for i, row in df.iterrows():

            id = str(row.get(ScriptColumn.INDEX, "")).strip()
            en = str(row.get(ScriptColumn.SCRIPT, "")).strip()
            vi = str(row.get(ScriptColumn.TRANSLATION, "")).strip()
            if not id or id.lower() == "nan":
                continue
            # skip empty row
            if not en and not vi:
                continue

            rows.append(
                ScriptRow(
                    id=id,
                    en=en,
                    vi=vi,
                )
            )

        return rows