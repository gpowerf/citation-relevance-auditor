# Zotero Integration

`scripts/zotero_fetch.py` pulls items from Zotero and outputs YAML compatible with the
agent pipeline (evidence_db.md or literature-scout template).

## Setup

```bash
pip install pyyaml
```

For local mode: `pip install pyyaml` (required for YAML output).
For API mode: `pip install pyzotero` and get an API key from https://www.zotero.org/settings/keys.

## Usage

### Local mode (reads zotero.sqlite directly — no API key needed)

Your database is expected at `~/Zotero/zotero.sqlite` by default.

```bash
# Fetch 20 most recent papers into evidence_db format
python scripts/zotero_fetch.py --local --limit 20

# Fetch from a specific collection into scout template format
python scripts/zotero_fetch.py --local --collection HRX69G3Z --limit 50 --format scout

# Specify a custom database path
python scripts/zotero_fetch.py --local --db /custom/path/zotero.sqlite

# Write output to file
python scripts/zotero_fetch.py --local --limit 50 --output papers.yaml
```

### API mode (requires pyzotero + API key)

```bash
python scripts/zotero_fetch.py --api-key YOUR_KEY --library-id 20407104

python scripts/zotero_fetch.py --api-key YOUR_KEY --library-id 20407104 \
  --collection HRX69G3Z --limit 20 --format scout
```

### Output formats

- `--format evidence` (default) — YAML matching `evidence_db.md` schema, ready to paste into `papers:` section
- `--format scout` — YAML matching the literature-scout template

## Pipeline workflow

1. `python scripts/zotero_fetch.py --local --limit 50 --output refs.yaml`
2. Open `evidence_db.md` and paste the YAML into the `papers:` section
3. Run the `@analyst` agent on each paper to extract claims
4. Run the `@drafter` agent with outline + evidence to write sections
5. Verify each citation with `@claim-verifier`

## Finding collection keys

```bash
python -c "
import sqlite3
conn = sqlite3.connect('$HOME/Zotero/zotero.sqlite')
c = conn.cursor()
c.execute('SELECT key, collectionName FROM collections')
for k, n in c.fetchall(): print(f'{n}: {k}')
conn.close()
"
```
