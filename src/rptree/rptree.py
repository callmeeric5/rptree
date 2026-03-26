import os
import pathlib
import sys

PIPE = "│"
ELBOW = "└──"
T = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "
DIR_ICON = "📁"
DEFAULT_FILE_ICON = "📄"
COLOR_RESET = "\033[0m"
DIR_COLOR = "\033[94m"
FILE_COLOR = "\033[92m"
ICON_MAP = {
    ".py": "🐍",
    ".md": "📝",
    ".txt": "📄",
    ".json": "🧩",
    ".yml": "🧾",
    ".yaml": "🧾",
    ".toml": "🧾",
    ".png": "🖼️",
    ".jpg": "🖼️",
    ".jpeg": "🖼️",
    ".gif": "🖼️",
    ".svg": "🖼️",
    ".pdf": "📕",
    ".zip": "🗜️",
    ".tar": "🗜️",
    ".gz": "🗜️",
    ".tgz": "🗜️",
}


class DirectoryTree:
    def __init__(
        self,
        root_dir,
        dir_only=False,
        output_file=sys.stdout,
        sort_tree=False,
        show_icons=False,
        use_color=False,
    ):
        self._output_file = output_file
        color_enabled = use_color and output_file == sys.stdout
        self._generator = _TreeGenerator(
            root_dir,
            dir_only,
            sort_tree=sort_tree,
            show_icons=show_icons,
            use_color=color_enabled,
        )

    def generate(self):
        tree = self._generator.build()
        is_file = self._output_file != sys.stdout

        if is_file:
            tree.insert(0, "```")
            tree.append("```")
            stream = open(str(self._output_file), mode="w", encoding="UTF-8")
        else:
            stream = sys.stdout

        try:
            for entry in tree:
                print(entry, file=stream)
        finally:
            if is_file:
                stream.close()


class _TreeGenerator:
    def __init__(
        self,
        root_dir,
        dir_only=False,
        sort_tree=False,
        show_icons=False,
        use_color=False,
    ):
        self._root_dir = pathlib.Path(root_dir)
        self._dir_only = dir_only
        self._sort_tree = sort_tree
        self._show_icons = show_icons
        self._use_color = use_color
        self._tree = []

    def build(self):
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self) -> None:
        name = f"{self._root_dir}{os.sep}"
        name = self._decorate_directory(name)
        self._tree.append(name)
        self._tree.append(PIPE)

    def _tree_body(self, directory, prefix=""):
        entries = self._prepare_entries(directory)
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else T
            if entry.is_dir():
                self._add_directory(
                    entry, index, entries_count, prefix, connector
                )
            else:
                self._add_file(entry, prefix, connector)

    def _prepare_entries(self, directory):
        entries = list(directory.iterdir())
        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()]
            if self._sort_tree:
                entries = sorted(
                    entries, key=lambda entry: entry.name.casefold()
                )
            return entries
        entries = sorted(entries, key=lambda entry: entry.is_file())
        if self._sort_tree:
            entries = sorted(
                entries,
                key=lambda entry: (entry.is_file(), entry.name.casefold()),
            )
        return entries

    def _add_directory(self, directory, idx, count, prefix, connector):
        name = f"{directory.name}{os.sep}"
        name = self._decorate_directory(name)
        self._tree.append(f"{prefix}{connector} {name}")
        if idx != count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(
            directory=directory,
            prefix=prefix,
        )
        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector):
        name = self._decorate_file(file.name, file)
        self._tree.append(f"{prefix}{connector} {name}")

    def _decorate_directory(self, name):
        label = f"{DIR_ICON} {name}" if self._show_icons else name
        return self._colorize(label, DIR_COLOR)

    def _decorate_file(self, name, file_path):
        icon = self._file_icon(file_path)
        label = f"{icon} {name}" if self._show_icons else name
        return self._colorize(label, FILE_COLOR)

    def _file_icon(self, file_path):
        if not self._show_icons:
            return ""
        ext = file_path.suffix.lower()
        return ICON_MAP.get(ext, DEFAULT_FILE_ICON)

    def _colorize(self, text, color_code):
        if not self._use_color:
            return text
        return f"{color_code}{text}{COLOR_RESET}"
