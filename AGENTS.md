# mount-image-hdiutil — AGENTS.md

## Project

Disk image mounting via hdiutil (macOS).

- **Package**: `mount-image-hdiutil` (PyPI), `mount_image_hdiutil` (import)
- **Repo**: `https://github.com/MBanucu/mount-image-hdiutil`
- **Python**: `>=3.10`
- **License**: GPL-3.0-only

## Commands

```bash
pip install -e .
python -m unittest discover -s tests -v
pip install coverage
python -m coverage run -m unittest discover -s tests -v
python -m coverage report --fail-under=70 --skip-covered
```

## Module structure

```
mount_image_hdiutil/
  __init__.py    — public API
tests/
  test_mount_image_hdiutil.py
```
