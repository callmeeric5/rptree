# distillation-rptree
RP Tree is a fast, simple directory tree generator with optional sorting,
icons, and colorized output.

## Features
- Directory-only mode
- Optional sorting (directories first, then files, alphabetically)
- Optional icons for folders and common file types
- Optional ANSI color output (stdout only)
- Write output to a file

## Install
From PyPI:
```bash
pip install distillation-rptree
```

From TestPyPI:
```bash
pip install -i https://test.pypi.org/simple/ distillation-rptree
```

## CLI Usage
After installation, the CLI is available as `rptree`:
```bash
rptree .
rptree . --sort-tree --icons --color
rptree . --dir-only
rptree . -o tree.md
```

To run from source without installing:
```bash
python -m distillation_rptree.cli .
```

### Options
```
usage: tree [-h] [-v] [-d] [-o [OUTPUT_FILE]] [-s] [--icons] [--color] [ROOT_DIR]

RP Tree, a directory tree generator

positional arguments:
  ROOT_DIR              Generate a full directory tree starting at ROOT_DIR

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -d, --dir-only        Generate a directory-only tree
  -o, --output-file [OUTPUT_FILE]
                        Generate a full directory tree and save it to a file
  -s, --sort-tree       Sort directories and files alphabetically within each level
  --icons               Show icons for directories and files
  --color               Use ANSI colors in the tree output (stdout only)

Thanks for using RP Tree!
```

## Python API
```python
from distillation_rptree.rptree import DirectoryTree

tree = DirectoryTree(
    ".",
    dir_only=False,
    output_file=None,
    sort_tree=True,
    show_icons=True,
    use_color=True,
)
tree.generate()
```

Note: `use_color` only applies when printing to stdout.

## Development
Build the package:
```bash
uv run python -m build
```

## License
MIT
