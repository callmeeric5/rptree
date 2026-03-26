import argparse
import pathlib
import sys

from . import __version__
from .rptree import DirectoryTree


def main():
    args = parse_cmd_line_arguments()
    root_dir = pathlib.Path(args.root_dir)
    if not root_dir.is_dir():
        print("The specified root directory doesn't exist")
        sys.exit()
    tree = DirectoryTree(
        root_dir,
        dir_only=args.dir_only,
        output_file=args.output_file,
        sort_tree=args.sort_tree,
        show_icons=args.icons,
        use_color=args.color,
    )
    tree.generate()


def parse_cmd_line_arguments():
    parser = argparse.ArgumentParser(
        prog="tree",
        description="RP Tree, a directory tree generator",
        epilog="Thanks for using RP Tree!",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"RP Tree v{__version__}"
    )

    parser.add_argument(
        "root_dir",
        metavar="ROOT_DIR",
        nargs="?",
        default=".",
        help="Generate a full directory tree starting at ROOT_DIR",
    )
    parser.add_argument(
        "-d",
        "--dir-only",
        action="store_true",
        help="Generate a directory-only tree",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        metavar="OUTPUT_FILE",
        nargs="?",
        default=sys.stdout,
        help="Generate a full directory tree and save it to a file",
    )
    parser.add_argument(
        "-s",
        "--sort-tree",
        action="store_true",
        help="Sort directories and files alphabetically within each level",
    )
    parser.add_argument(
        "--icons",
        action="store_true",
        help="Show icons for directories and files",
    )
    parser.add_argument(
        "--color",
        action="store_true",
        help="Use ANSI colors in the tree output (stdout only)",
    )
    return parser.parse_args()
