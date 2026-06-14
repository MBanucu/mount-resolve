"""Cross-platform block device and mount point resolution.

Resolves file paths to their underlying block device, mount point, and
filesystem type on Linux and macOS.
"""

from mount_resolve._resolve import (
    resolve_device,
    resolve_mount_point,
    _df_output,
    resolve,
)
from mount_resolve._resolve_linux import device_backing_file as _linux_backing
from mount_resolve._resolve_darwin import device_backing_file as _darwin_backing

import platform

device_backing_file = _darwin_backing if platform.system() == 'Darwin' else _linux_backing

__all__ = [
    'resolve_device',
    'resolve_mount_point',
    '_df_output',
    'resolve',
    'device_backing_file',
]
