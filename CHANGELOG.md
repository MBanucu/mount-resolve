# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-06-14

### Added

- `resolve_device(path)` — resolve a file path to its underlying block device.
- `resolve_mount_point(path)` — resolve a file path to its mount point.
- `_df_output(path)` — raw df output as `(device, mount_point, fstype)` tuple.
- `resolve(path)` — combined call returning `(device, mount_point, fstype)`.
- Linux support via `/proc/partitions`, `/sys/dev/block`, and `findmnt`.
- macOS support via `df`, `stat`, and `hdiutil info -plist`.
- Nix flake with dev shell and package overlay.

[unreleased]: https://github.com/MBanucu/mount-resolve/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/MBanucu/mount-resolve/releases/tag/v0.1.0
