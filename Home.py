from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Paths to the models
MODEL1_PATH = "DenseNet_121_Aug2_MD.h5"
MODEL2_PATH = "densenet_MODEL_ORG_80_20.h5"

# Class labels for each model
MODEL1_LABELS = ['Alternaria', 'Downey Mildew', 'Powdrey Mildew', 'White Rust']
MODEL2_LABELS = ['Alternaria Leaf Spot', 'Cercospora', 'Phyllody', 'Phytopthora']

@app.route('/')
def home():
    return render_template('index.html')

# Common image preprocessing function
def preprocess_image(file):
    image = Image.open(file).resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Empty file name'}), 400

        image = preprocess_image(file)

        # Use MODEL1 for prediction (you can switch to MODEL2 if needed)
        model = tf.keras.models.load_model(MODEL1_PATH)
        predictions = model.predict(image)

        class_idx = int(np.argmax(predictions))
        confidence = float(np.max(predictions))
        class_label = MODEL1_LABELS[class_idx] if class_idx < len(MODEL1_LABELS) else "Unknown"

        return jsonify({'prediction': class_label, 'confidence': confidence})

    except Exception as e:
        # Print to server logs and return JSON error
        print(f"Error in /predict: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
