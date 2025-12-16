from flask import (
    Flask,
    Response,
    flash,
    redirect,
    render_template,
    request,
    stream_with_context,
)

import re, os, json

from tempfile import TemporaryDirectory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

_ALLOWED_EXTENSIONS_RE = re.compile(
    r"\.(ts|js|tsx|jsx)$",
    re.IGNORECASE,
)


def js_escape(s: str) -> str:

    # Safely embed HTML into JS string
    return json.dumps(s)


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

    # Read file safely
    try:
        content = user_input or process_uploaded_file(file)
    except Exception as e:
        return render_template("analysis.html", error=str(e))

    @stream_with_context
    def generate():
        from markdown_it import MarkdownIt
        from bs4 import BeautifulSoup

        yield render_template("analysis.html", initial_html="")

        # Try importing analyze()
        try:
            from analyze import analyze
        except ImportError:
            try:
                from .analyze import analyze
            except ImportError:
                yield '<div class="error">Analysis module not found</div>'
                return

        markdown = MarkdownIt("gfm-like")
        full_markdown = ""

        # Run analysis
        try:
            for chunk in analyze(content):
                full_markdown += chunk
            parsed = markdown.render(full_markdown)
            soup = BeautifulSoup(parsed, "html.parser")
            for pre in soup.find_all("pre"):
                pre.attrs.pop("tabindex", None)
            html = str(soup)

            yield html

            # Completion message
            yield "<div class='success'><strong>✅ Analysis complete!</strong></div>"

        except Exception as e:
            yield f'<div class="error">Error during analysis: {str(e)}</div>'
            return

    return Response(generate(), mimetype="text/html")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
