import argparse
import os
import sys

try:
    import libtorrent as lt
except ImportError:
    print("This script requires the python bindings for libtorrent.", file=sys.stderr)
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(description="Create a .torrent file")
    parser.add_argument("source", help="Path to file or directory to share")
    parser.add_argument("-o", "--output", help="Path to output .torrent file")
    parser.add_argument("--piece-size", type=int, default=0, help="Piece size in bytes (0 for auto)")
    parser.add_argument("--private", action="store_true", help="Mark torrent as private")
    parser.add_argument("--tracker", action="append", default=[], help="Add tracker URL")
    parser.add_argument("--web-seed", action="append", default=[], help="Add web seed URL")
    parser.add_argument("--comment", default="", help="Add comment")
    parser.add_argument("--source-string", default="", help="Set source field")
    parser.add_argument("--format", choices=["v1", "v2", "hybrid"], help="Torrent format (libtorrent 2.x)")
    parser.add_argument("--optimize-alignment", action="store_true", help="Use optimize_alignment flag (libtorrent 1.x)")
    parser.add_argument("--padded-file-size-limit", type=int, default=0, help="padded_file_size_limit in bytes (libtorrent 1.x)")
    return parser.parse_args()


def create_torrent(args):
    fs = lt.file_storage()
    lt.add_files(fs, os.path.abspath(args.source), lambda f: not os.path.basename(f).startswith('.'))

    flags = lt.create_flags_t()
    lt_version = tuple(int(x) for x in lt.__version__.split('.')[:2]) if hasattr(lt, '__version__') else (0,)
    if lt_version and lt_version[0] >= 2:
        format_map = {
            None: lt.create_torrent.flags_t(0),
            'v1': lt.create_torrent.v1_only,
            'v2': lt.create_torrent.v2_only,
            'hybrid': lt.create_torrent.flags_t(0)
        }
        torrent = lt.create_torrent(fs, args.piece_size, flags | format_map.get(args.format, lt.create_torrent.flags_t(0)))
    else:
        if args.optimize_alignment:
            flags |= lt.create_torrent.optimize_alignment
        torrent = lt.create_torrent(fs, args.piece_size, args.padded_file_size_limit, flags)

    for t in args.tracker:
        torrent.add_tracker(t)
    for s in args.web_seed:
        torrent.add_url_seed(s)

    torrent.set_comment(args.comment)
    torrent.set_creator("qBittorrent console creator")
    torrent.set_priv(args.private)

    lt.set_piece_hashes(torrent, os.path.dirname(os.path.abspath(args.source)))

    entry = torrent.generate()
    if args.source_string:
        entry['info']['source'] = args.source_string

    torrent_data = lt.bencode(entry)
    output = args.output or os.path.basename(os.path.abspath(args.source)) + '.torrent'
    with open(output, 'wb') as f:
        f.write(torrent_data)
    print(f"Torrent file created: {output}")


def main():
    args = parse_args()
    create_torrent(args)


if __name__ == "__main__":
    main()
