from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
)
import re, os
from tempfile import TemporaryDirectory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

_ALLOWED_EXTENSIONS_RE = re.compile(
    r"\.(ts|js|tsx|jsx)$",
    re.IGNORECASE,
)


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


app = Flask(__name__)
app.config.from_mapping(SECRET_KEY="dev")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


@app.route("/", methods=["GET"])
def home():
    return render_template("file_upload.html")


@app.route("/", methods=["POST"])
def upload_and_analyze():
    file = request.files.get("file")
    user_input = request.form.get("user-input")

    if not file and not user_input:
        flash("No data, please upload a file or paste your code")
        return redirect("/")

    if file and not allowed_file(file.filename):
        flash("File type not allowed. Please upload .ts, .js, .tsx, or .jsx files.")
        return redirect("/")

    try:
        content = user_input or process_uploaded_file(file)
    except Exception as e:
        return render_template("analysis.html", error=str(e))
    # Perform analysis
    try:
        from markdown_it import MarkdownIt

        try:
            from analyze import analyze
        except ImportError:
            try:
                from .analyze import analyze
            except ImportError:
                return render_template(
                    "analysis.html", error="Analysis module not found"
                )

        full_markdown = "".join(analyze(content))
        markdown = MarkdownIt("gfm-like")
        html = markdown.render(full_markdown)

    except Exception as e:
        return render_template("analysis.html", error=str(e))

    return render_template("analysis.html", analysis=html)
