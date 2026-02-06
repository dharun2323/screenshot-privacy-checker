import os
import cv2
import pytesseract
from flask import Flask, render_template, request
from detector import detect_sensitive

# Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# create uploads folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    detected = []

    if request.method == "POST":

        # 1️⃣ check file
        if "screenshot" not in request.files:
            return render_template("index.html", error="No file selected")

        file = request.files["screenshot"]

        if file.filename == "":
            return render_template("index.html", error="No file selected")

        # 2️⃣ save image
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(image_path)

        # 3️⃣ read image
        img = cv2.imread(image_path)

        # 4️⃣ SIMPLE OCR (NO OVER FILTERING)
        text = pytesseract.image_to_string(img)
        print("OCR TEXT >>>", repr(text))

        # 5️⃣ DECISION BASED ON OCR TEXT
        if text.strip() == "":
            result = "✅ Safe to Share"
            detected = []
        else:
            detected = detect_sensitive(text)

            if detected:
                result = "⚠️ Sensitive Information Detected!"
            else:
                result = "✅ Safe to Share"

    return render_template("index.html", result=result, detected=detected)

if __name__ == "__main__":
    app.run(debug=True)
