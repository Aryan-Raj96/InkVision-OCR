from flask import Flask, render_template, request, send_file
import cv2
import numpy as np
import easyocr
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static/output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Image Processing
def flatten_image(gray):
    blur = cv2.GaussianBlur(gray, (0,0), 15)
    return cv2.divide(gray, blur, scale=255)

def enhance_contrast(gray):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    return clahe.apply(gray)

@app.route("/")
def home():
    return render_template("index.html", show_result=False)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["image"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    img = cv2.imread(filepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    flat = flatten_image(gray)
    contrast = enhance_contrast(flat)

    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(contrast)

    all_words = [text for _, text, _ in results]

    # Draw bounding boxes
    output_img = cv2.cvtColor(contrast, cv2.COLOR_GRAY2BGR)
    for box, text, conf in results:
        pts = np.array(box, dtype=np.int32)
        cv2.polylines(output_img, [pts], True, (0,255,0), 2)
        x, y = pts[0]
        cv2.putText(output_img, text, (x, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0,0,255), 1)

    output_image_path = os.path.join(OUTPUT_FOLDER, "result.jpg")
    cv2.imwrite(output_image_path, output_img)

    # Generate PDF
    pdf_path = os.path.join(OUTPUT_FOLDER, "result.pdf")
    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>Extracted Text</b>", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    for word in all_words:
        elements.append(Paragraph(word, styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)

    return render_template(
        "index.html",
        raw_words=all_words,
        image_path="output/result.jpg",
        show_result=True
    )

@app.route("/download_pdf")
def download_pdf():
    return send_file("static/output/result.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
