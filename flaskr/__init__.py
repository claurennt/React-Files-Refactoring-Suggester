import os
import tempfile

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {"tsx", "jsx", "ts", "js"}


def allowed_file(filename):
    return filename in ALLOWED_EXTENSIONS


app = Flask(__name__)
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config.from_mapping(
    SECRET_KEY="dev",
)


@app.route("/")
def home():
    return render_template("file_upload.html")


@app.route("/", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        flash("No file part")
        app.logger.error("File upload error")
        return redirect(request.url)

    file = request.files["file"]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)
    _, file_extension = os.path.splitext(file.filename)
    # If the user uploads an invalid file type
    if file and allowed_file(file_extension):
        flash("File type not allowed, please only upload a valid JS file")
        return redirect(request.url)

    filename = secure_filename(file.filename)
    app.logger.info("%s logged in successfully", file)

    # Create a temporary file
    temp_dir = tempfile.mkdtemp()
    filename = secure_filename(file.filename)
    temp_path = os.path.join(temp_dir, filename)
    # Save the file
    file.save(temp_path)

    content = ""

    # Process the file
    with open(temp_path, "r") as f:
        content = f.read()

    # Clean up: remove temp file when done
    os.remove(temp_path)
    os.rmdir(temp_dir)
    from .analyze import analyze

    analysis = analyze(content)
    return render_template("analysis.html", analysis=analysis)
