from flask import Flask, request, jsonify
import joblib
from .data_loader import extract_text_from_pdf, extract_text_from_docx, extract_text_from_image
import os

app = Flask(__name__)



ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'docx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_model(model_path):
    relative_path = os.path.join(os.path.dirname(__file__), model_path)
    return joblib.load(relative_path)

def predict_file_class(model, file):
    if file.filename.endswith('.pdf'):
        text = extract_text_from_pdf(file)
    elif file.filename.endswith('.docx'):
        text = extract_text_from_docx(file)
    elif file.filename.endswith('.jpg') or file.filename.endswith('.jpeg') or file.filename.endsWith('.png'):
        text = extract_text_from_image(file)
    else:
        raise ValueError("Unsupported file type")

    prediction = model.predict([text])
    return prediction[0]

@app.route('/classify_file', methods=['POST'])
def classify_file_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file in the request"}), 400

    files = request.files.getlist('file')  
    
    if not files or all(file.filename == '' for file in files):
        return jsonify({"error": "No selected files"}), 400
    
    

    model = load_model('../models/model.pkl')  

    results = []
    for file in files:
        if not allowed_file(file.filename):
            results.append({"filename": file.filename, "error" : "Unsupported file type"}) 
            continue  
        predicted_class = predict_file_class(model, file)
        results.append({"filename": file.filename, "file_class": predicted_class})

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)