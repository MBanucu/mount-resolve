# mount-resolve

[![PyPI version](https://img.shields.io/pypi/v/mount-resolve)](https://pypi.org/project/mount-resolve/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://www.python.org/)
[![License](https://img.shields.io/github/license/MBanucu/mount-resolve)](LICENSE)
[![OS](https://img.shields.io/badge/OS-Linux%20%7C%20macOS-blue)](https://github.com/MBanucu/mount-resolve)

[![CI](https://img.shields.io/github/actions/workflow/status/MBanucu/mount-resolve/test.yml?branch=main)](https://github.com/MBanucu/mount-resolve/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/MBanucu/mount-resolve/branch/main/graph/badge.svg)](https://codecov.io/gh/MBanucu/mount-resolve)

Cross-platform block device and mount point resolution from file paths.

## Features

- **`resolve_device`** — find the underlying block device for any file path
  (Linux `/proc/partitions` + `/sys/dev/block`, macOS `hdiutil`)
- **`resolve_mount_point`** — find the mount point for any file path
  (Linux `findmnt`, macOS `df`)
- **`resolve`** — combined call returning `(device, mount_point, fstype)`

## Quick start

```python
from mount_resolve import resolve, resolve_device, resolve_mount_point

# Combined — get device, mount point, and filesystem type in one call
info = resolve('/some/file')
# ('/dev/sda1', '/', 'ext4')

# Individual
device = resolve_device('/some/file')
mount = resolve_mount_point('/some/file')
```

## License

GPL-3.0-only
