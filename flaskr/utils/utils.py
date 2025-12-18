import re, os
from tempfile import TemporaryDirectory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

_ALLOWED_EXTENSIONS_RE = re.compile(
    r"\.(ts|js|tsx|jsx)$",
    re.IGNORECASE,
)


def sanitize_input(user_input: str):
    # Regular expression to blocklist script tags
    sanitized_str = re.sub(
        r"<script\b[^>]*>(.*?)</script>", "", user_input, flags=re.IGNORECASE
    )
    return sanitized_str


def process_uploaded_file(file: FileStorage):
    with TemporaryDirectory() as temp_dir:
        secured_filename = secure_filename(file.filename)
        path = os.path.join(temp_dir, secured_filename)
        file.save(path)

        with open(path, "r", encoding="utf-8") as f:
            return f.read()


def allowed_file(
    filename: str, extensions: tuple[str, ...] = _ALLOWED_EXTENSIONS_RE
) -> bool:
    """Check if file has an allowed extension using a cached regex."""
    return bool(extensions.search(filename))
