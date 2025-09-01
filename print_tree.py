# print_tree.py
from pathlib import Path

# Folders/files to exclude anywhere in the tree
EXCLUDE_DIRS = {".git", "venv", "__pycache__", "node_modules", "staticfiles"}
EXCLUDE_FILE_SUFFIXES = {".pyc", ".pyo", ".pyd", ".sqlite3", ".log"}

def is_excluded(path: Path) -> bool:
    # Exclude by directory name anywhere in the path
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    # Exclude by file extension
    if path.is_file() and path.suffix in EXCLUDE_FILE_SUFFIXES:
        return True
    return False

def print_tree(dir_path: Path, prefix: str = ""):
    # sort: directories first, then files; both alphabetically
    entries = sorted(
        [p for p in dir_path.iterdir() if not is_excluded(p)],
        key=lambda p: (p.is_file(), p.name.lower())
    )
    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        line = prefix + connector + entry.name + ("/" if entry.is_dir() else "")
        print(line)
        if entry.is_dir():
            extension = "    " if i == len(entries) - 1 else "│   "
            print_tree(entry, prefix + extension)

if __name__ == "__main__":
    root = Path.cwd()
    print(f"{root.name}/")
    print_tree(root)
