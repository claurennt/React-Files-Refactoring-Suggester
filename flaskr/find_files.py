import os


def find_files_in_dir(
    dir_path: str = ".",
    file_extensions: tuple[str, ...] = (".tsx", ".jsx"),
    ignored_directories: tuple[str, ...] = (
        "node_modules",
        "__tests__",
        "dist",
        "build",
    ),
):
    """Return a list of source files of a certain extensions(s) under a certain dir_path."""

    for root, dirs, files in os.walk(dir_path):
        # Prevent descending into ignored directories and any hidden dirs
        ignored_set = {name.lower() for name in ignored_directories}
        dirs[:] = [
            dir
            for dir in dirs
            if not dir.startswith(".") and dir.lower() not in ignored_set
        ]
        for file in files:
            _, file_extension = os.path.splitext(file)
            if file_extension in file_extensions:
                file = os.path.join(root, file)
                yield file


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="FileFinder",
        description="Find files of given extensions in directory",
    )
    parser.add_argument("path", nargs="?", default=".", help="Directory to scan")
    parser.add_argument(
        "-e",
        "--extensions",
        nargs="+",
        default=[".tsx", ".jsx", ".js", ".ts"],
        help="File extensions to include (e.g. .tsx .jsx .ts .js)",
    )
    parser.add_argument(
        "-ignored",
        "--ignored_directories",
        nargs="+",
        default=["node_modules", "__tests__", "dist", "build"],
        help="Directories to ignore (e.g. .git node_modules)",
    )

    args = parser.parse_args()
    exts = tuple(args.extensions)
    ignored_dirs = tuple(args.ignored_directories)
    found = list(
        find_files_in_dir(
            args.path, file_extensions=exts, ignored_directories=ignored_dirs
        )
    )

    print(f"Found {len(found)} files in {os.path.abspath(args.path)}")
    for file in found:
        print(file)
