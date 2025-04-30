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

@app.route('/predict_model1', methods=['POST'])
def predict_model1():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']
    image = preprocess_image(file)

    model = tf.keras.models.load_model(MODEL1_PATH)
    predictions = model.predict(image)
    class_idx = np.argmax(predictions)
    confidence = np.max(predictions)
    class_label = MODEL1_LABELS[class_idx] if class_idx < len(MODEL1_LABELS) else "Unknown"

    return jsonify({'prediction': class_label, 'confidence': float(confidence)})

@app.route('/predict_model2', methods=['POST'])
def predict_model2():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']
    image = preprocess_image(file)

    model = tf.keras.models.load_model(MODEL2_PATH)
    predictions = model.predict(image)
    class_idx = np.argmax(predictions)
    confidence = np.max(predictions)
    class_label = MODEL2_LABELS[class_idx] if class_idx < len(MODEL2_LABELS) else "Unknown"

    return jsonify({'prediction': class_label, 'confidence': float(confidence)})

if __name__ == '__main__':
    app.run(debug=True)
