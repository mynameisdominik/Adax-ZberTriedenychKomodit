# Adax-ZberTriedenychKomodit

Standalone parser for collection calendars published by ADAX spol. s r.o.

The project reads public DOCX calendars and returns collection dates for:

- `Plast, VKM, Kov ob.`
- `Papier`

It is independent from Home Assistant and from `hacs_waste_collection_schedule`.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

## Usage

```powershell
adax-calendar "https://www.obecvieska.sk/evt_file.php?file=2590"
```

The output is JSON, for example:

```json
{
  "date": "2026-01-29",
  "commodity": "Papier"
}
```

## Test

```powershell
python -m pytest
```
