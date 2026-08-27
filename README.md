# Adax-ZberTriedenychKomodit

Home Assistant integration for collection calendars published by ADAX spol. s r.o.

The project reads public DOCX calendars and returns collection dates for:

- `Plast, VKM, Kov ob.`
- `Papier`

This is a standalone repository and is independent from `hacs_waste_collection_schedule`.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

## Home Assistant setup

Install this repository through HACS as a custom repository with type **Integration**.
After restarting Home Assistant, add **ADAX Zber triedených komodít** through
Settings > Devices & services > Add integration. Enter the municipality and its
public DOCX calendar URL.

The integration creates two sensors with the next collection date in the
`next_collection` attribute:

- `Plast, VKM, Kov ob.`
- `Papier`

## Command-line usage

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
