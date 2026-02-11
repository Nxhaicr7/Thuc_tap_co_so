from flask import Flask, render_template, request, url_for, jsonify
from Inference import inference_from_path, inference_from_base64
import os
from werkzeug.utils import secure_filename
from PIL import Image
import base64
from io import BytesIO
from datetime import datetime

# Initialize Flask and saving photo folder
app = Flask(__name__, static_folder='static')
app.config["UPLOAD_FOLDER"] = "static"

# Constants for validation
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MIN_IMAGE_DIMENSION = 100  # Minimum width/height in pixels
MAX_IMAGE_DIMENSION = 2000  # Maximum width/height in pixels

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image_dimensions(image):
    width, height = image.size
    if width < MIN_IMAGE_DIMENSION or height < MIN_IMAGE_DIMENSION:
        return False, "Image dimensions are too small (minimum 100x100 pixels)"
    if width > MAX_IMAGE_DIMENSION or height > MAX_IMAGE_DIMENSION:
        return False, "Image dimensions are too large (maximum 2000x2000 pixels)"
    return True, None

@app.route("/", methods=["GET", "POST"])
def index():
    current_time = datetime.now().strftime("%I:%M %p, %B %d, %Y")
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("index.html", error="No file uploaded", current_time=current_time), 400
        file = request.files["file"]
        if file.filename == "":
            return render_template("index.html", error="No selected file", current_time=current_time), 400

        if not allowed_file(file.filename):
            return render_template("index.html", error="Invalid file format. Only PNG, JPG, JPEG allowed", current_time=current_time), 400

        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        if file_size > MAX_FILE_SIZE:
            return render_template("index.html", error="File size exceeds 5MB limit", current_time=current_time), 400
        file.seek(0)

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        try:
            image = Image.open(filepath)
            is_valid, error_message = validate_image_dimensions(image)
            if not is_valid:
                os.remove(filepath)
                return render_template("index.html", error=error_message, current_time=current_time), 400
        except Exception as e:
            os.remove(filepath)
            return render_template("index.html", error=f"Error processing image: {str(e)}", current_time=current_time), 400

        try:
            label, score, resized_image_path = inference_from_path(filepath)
            resized_image_url = url_for('static', filename=os.path.basename(resized_image_path))
            return render_template("index.html", prediction=f"{label} ({score:.2f})", image_url=resized_image_url, current_time=current_time)
        except Exception as e:
            return render_template("index.html", error=f"Error during inference: {str(e)}", current_time=current_time), 500

    return render_template("index.html", current_time=current_time)

@app.route("/webcam")
def webcam():
    return render_template("webcam.html")

@app.route("/api/predict_webcam", methods=["POST"])
def predict_webcam():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "No image data"}), 400

    try:
        base64_data = data["image"].split(",")[1]
        if not base64_data:
            return jsonify({"error": "Empty image data"}), 400
    except IndexError:
        return jsonify({"error": "Invalid base64 image format"}), 400

    try:
        image_data = base64.b64decode(base64_data)
        image = Image.open(BytesIO(image_data))
        if image.format.lower() not in ALLOWED_EXTENSIONS:
            return jsonify({"error": "Invalid image format. Only PNG, JPG, JPEG allowed"}), 400
        is_valid, error_message = validate_image_dimensions(image)
        if not is_valid:
            return jsonify({"error": error_message}), 400
        label, score = inference_from_base64(base64_data)
        return jsonify({"label": label, "score": f"{score:.2f}"})
    except base64.binascii.Error:
        return jsonify({"error": "Invalid base64 encoding"}), 400
    except Exception as e:
        return jsonify({"error": f"Error processing image: {str(e)}"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)