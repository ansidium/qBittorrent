Console torrent creation
=======================

The `create_torrent.py` script provides a command line interface to generate `.torrent` files using the libtorrent Python bindings.

### Usage

```bash
python3 scripts/create_torrent.py [options] <source>
```

Key options:

- `-o`, `--output` – path to save the resulting `.torrent` (defaults to `<source>.torrent`).
- `--piece-size` – piece size in bytes (`0` for automatic selection).
- `--tracker` – specify tracker URL (may be used multiple times).
- `--web-seed` – specify web seed URL (may be used multiple times).
- `--private` – mark the torrent as private.
- `--comment` – add a comment to the torrent.
- `--source-string` – set the `source` field.
- `--format` – select torrent format when using libtorrent 2.x (`v1`, `v2`, or `hybrid`).
- `--optimize-alignment` and `--padded-file-size-limit` – options for libtorrent 1.x.

The script requires the `libtorrent` Python package to be installed.
