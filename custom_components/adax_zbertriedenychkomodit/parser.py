from __future__ import annotations

import io
import re
from dataclasses import dataclass
from datetime import date

import requests
from docx import Document

from .const import PAPER_COMMODITY, PLASTIC_COMMODITY

_DATE_PATTERN = re.compile(r"\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b")


@dataclass(frozen=True)
class Collection:
    date: date
    commodity: str


def parse_url(url: str, *, timeout: int = 30) -> list[Collection]:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return parse_docx(response.content)


def parse_docx(source: bytes | str) -> list[Collection]:
    document = Document(io.BytesIO(source) if isinstance(source, bytes) else source)
    for table in document.tables:
        if not table.rows:
            continue
        columns = {
            index: _commodity(cell.text)
            for index, cell in enumerate(table.rows[0].cells)
            if _commodity(cell.text) is not None
        }
        if not columns:
            continue
        result = []
        for row in table.rows[1:]:
            for index, commodity in columns.items():
                if index >= len(row.cells):
                    continue
                for match in _DATE_PATTERN.finditer(row.cells[index].text):
                    result.append(
                        Collection(
                            date(
                                int(match.group(3)),
                                int(match.group(2)),
                                int(match.group(1)),
                            ),
                            commodity,
                        )
                    )
        if result:
            return result
    raise ValueError("No supported ADAX commodity table found")


def _commodity(header: str) -> str | None:
    normalized = " ".join(header.casefold().split())
    if "papier" in normalized:
        return PAPER_COMMODITY
    if all(value in normalized for value in ("plast", "vkm", "kov")):
        return PLASTIC_COMMODITY
    return None
