# Scripts

This directory contains repository-maintenance scripts for validating and
updating the generated model layer against the Google Wallet discovery
document.

## `check_api_up_to_date.py`

Compares the local Pydantic models against the Google Wallet discovery schema.
It validates:

- model/type coverage,
- field presence and type compatibility,
- enum value coverage,
- API deprecation markers,
- field docstring format lines such as `int64 format`, and
- optionally class/field docstring text.

Examples:

```sh
.venv/bin/python scripts/check_api_up_to_date.py \
  --offline scripts/google-wallet-api.json \
  --no-docstrings

.venv/bin/python scripts/check_api_up_to_date.py \
  --offline scripts/google-wallet-api.json
```

The script fetches the current API discovery document from
https://walletobjects.googleapis.com/$discovery/rest?version=v1 if the
`--offline` option is omitted.

## `sync_docstrings_from_discovery.py`

Synchronizes model docstrings from the discovery document while preserving the
original Python formatting via `libcst`.

The script updates:

- `BaseModel` class docstrings,
- model field docstrings attached to annotated assignments, and
- enum-member docstrings when the discovery schema exposes `enumDescriptions`
  (for example legacy alias enum values).

Behavior:

- Dry-run by default: prints planned changes and exits with status `1` when
  changes would be made.
- `--write`: applies the changes in place.
- `--mode fill-missing`: only inserts missing docstrings.
- `--mode overwrite`: replaces differing docstrings from discovery.
- `--mode interactive`: prompts per file before writing; requires `--write`.
- Conflicting wildcard-schema descriptions are reported and skipped for manual
  resolution.

Examples:

```sh
.venv/bin/python scripts/sync_docstrings_from_discovery.py \
  --offline scripts/google-wallet-api.json

.venv/bin/python scripts/sync_docstrings_from_discovery.py \
  --offline scripts/google-wallet-api.json \
  --write \
  --mode overwrite
```

The script fetches the current API discovery document from
https://walletobjects.googleapis.com/$discovery/rest?version=v1 if the
`--offline` option is omitted.

Recommended workflow:

1. Run the sync script in dry-run mode against the offline snapshot.
2. Inspect the planned changes and any reported conflicts.
3. Re-run with `--write` once the output looks correct.
4. Finish with `check_api_up_to_date.py` to confirm docstrings and format lines
   now match the discovery data.