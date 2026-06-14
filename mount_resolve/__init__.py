"""Cross-platform block device and mount point resolution.

Resolves file paths to their underlying block device, mount point, and
filesystem type on Linux and macOS.
"""

from mount_resolve._resolve import resolve_device, resolve_mount_point, _df_output, resolve

__all__ = [
    'resolve_device',
    'resolve_mount_point',
    '_df_output',
    'resolve',
]
