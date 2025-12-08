import os

from flask import Flask, render_template


def create_app():

    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    @app.route("/")
    def home():
        return render_template("file_upload.html")

    return app


app = create_app()
