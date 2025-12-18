from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
)

import os


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key-for-local-only")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


@app.errorhandler(413)
def too_large():
    flash("File too large (max 16MB).")
    return redirect("/")


@app.route("/", methods=["GET"])
def home():
    return render_template("file_upload.html")


@app.route("/", methods=["POST"])
def upload_and_analyze():
    from flaskr.utils.utils import allowed_file, process_uploaded_file, sanitize_input

    file = request.files.get("file")
    user_input = request.form.get("user-input").strip()

    if not file and not user_input:
        flash("No data, please upload a file or paste your code")
        return redirect("/")

    if file and not allowed_file(file.filename):
        flash("File type not allowed. Please upload .ts, .js, .tsx, or .jsx files.")
        return redirect("/")

    try:
        input = user_input or process_uploaded_file(file)
        content = sanitize_input(input)
    except Exception as e:
        return render_template("analysis.html", error=str(e))
    # Perform analysis
    try:
        from markdown_it import MarkdownIt
        from .analyze import analyze

        full_markdown = "".join(analyze(content))
        markdown = MarkdownIt("gfm-like")
        html = markdown.render(full_markdown)

    except Exception as e:
        return render_template("analysis.html", error=str(e))

    return render_template("analysis.html", analysis=html)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
