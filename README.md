# InkVision-OCR
AI-powered handwritten text extraction web application using Flask, EasyOCR and OpenCV .
## Features

* Extract handwritten and printed text from images
* Image preprocessing using OpenCV
* OCR using EasyOCR
* Bounding boxes drawn around detected text
* Download extracted text as PDF

## Tech Stack

* Python
* Flask
* EasyOCR
* OpenCV
* HTML
* CSS

## How it Works

1. Upload an image containing handwritten text.
2. The system preprocesses the image to enhance contrast.
3. EasyOCR extracts the text from the image.
4. Detected text is displayed with bounding boxes.
5. The extracted text can be downloaded as a PDF.

## Installation

Install required libraries:

pip install flask easyocr opencv-python numpy reportlab

Run the application:

python app.py

Open in browser:

http://127.0.0.1:5000

## Author

Aryan Raj

