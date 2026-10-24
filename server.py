"""Flask web application for the Emotion Detection project."""

import subprocess
import sys

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

def run_static_code_analysis():
    """Run Pylint on the Flask server."""
    result = subprocess.run(
        [sys.executable, "-m", "pylint", "server.py"],
        capture_output=True,
        text=True,
        check=False
    )
    print(result.stdout)
    print(result.stderr)
    return result.returncode

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """Render the page and handle emotion detection requests."""
    result = None
    text_to_analyze = ""
    error_message = None

    if request.method == "POST":
        text_to_analyze = request.form.get("textToAnalyze", "")

        if not text_to_analyze.strip():
            error_message = "Please enter some text to analyze."
        else:
            result = emotion_detector(text_to_analyze)

            if result is None:
                error_message = (
                    "Emotion detection could not be completed. "
                    "The NLP service may be unavailable."
                )

    return render_template(
        "index.html",
        result=result,
        text_to_analyze=text_to_analyze,
        error_message=error_message
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
