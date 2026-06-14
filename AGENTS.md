# mount-resolve — AGENTS.md

## Project

Cross-platform block device and mount point resolution from file paths.

- **Package**: `mount-resolve` (PyPI), `mount_resolve` (import)
- **Repo**: `https://github.com/MBanucu/mount-resolve`
- **Python**: `>=3.10`
- **License**: GPL-3.0-only

## Commands

```bash
# Install (editable)
pip install -e .

# Run tests
python -m unittest discover -s tests -v

# Run tests with coverage
pip install coverage
python -m coverage run -m unittest discover -s tests -v
python -m coverage report --fail-under=70 --skip-covered

# Coverage per-file JSON dump
python -m coverage json -o cov.json
```

CI workflow: `.github/workflows/test.yml` — matrix on `ubuntu-latest` and `macos-latest` × Python 3.10–3.14.

## Coverage — Codecov API

Coverage data is uploaded per-runner and merged by Codecov. Query programmatically via the Codecov v2 REST API (no auth needed for public repos).

### Commit/branch coverage report (per-file totals + line-by-line)

```
GET https://api.codecov.io/api/v2/github/{owner}/repos/{repo}/report/?branch=main
GET https://api.codecov.io/api/v2/github/{owner}/repos/{repo}/report/?sha={sha}
```

For mount-resolve:
```
https://api.codecov.io/api/v2/github/MBanucu/repos/mount-resolve/report/?branch=main
```

### Response shape

```json
{
  "totals": {
    "coverage": 93.38,
    "hits": 494,
    "misses": 35,
    "lines": 529,
    "partials": 0,
    "files": 10
  },
  "files": [
    {
      "name": "mount_resolve/_resolve.py",
      "totals": {
        "coverage": 100.0,
        "hits": 36,
        "misses": 0,
        "lines": 36
      },
      "line_coverage": [
        [8, 0],
        [9, 0],
        [10, 0],
        [13, 0]
      ]
    }
  ]
}
```

Each entry in `line_coverage` is `[line_number, status]` where:
- `0` = hit (covered)
- `1` = miss (uncovered)
- `2` = partial

Full API reference: `https://docs.codecov.com/llms.txt`

## Module structure

```
mount_resolve/
  __init__.py         — public API re-exports
  _resolve.py         — cross-platform df-based resolution + dispatcher
  _resolve_linux.py   — Linux-specific (os.stat + /proc/partitions + findmnt)
  _resolve_darwin.py  — macOS-specific (df + hdiutil + plistlib)
tests/
  test_mount_resolve.py — unit + mocked tests
```
