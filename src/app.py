from flask import Flask, request, jsonify
import joblib
import PyPDF2

from src.classifier import classify_file
app = Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg'}

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file) 
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def load_model(model_path):
    return joblib.load(model_path)

def predict_file_class(model, file):
    text = extract_text_from_pdf(file)  
    prediction = model.predict([text])
    return prediction[0]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/classify_file', methods=['POST'])
def classify_file_route():

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    model = load_model('/Users/bradleyweaver/Documents/heron/join-the-siege/models/model.pkl')  # Load your trained model
    predicted_class = predict_file_class(model, file)


    return jsonify({"file_class": predicted_class}), 200


if __name__ == '__main__':
    app.run(debug=True)
