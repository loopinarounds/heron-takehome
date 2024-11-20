import os
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib 

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def load_data(data_dir):
    texts = []
    labels = []
    for file_name in os.listdir(data_dir):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(data_dir, file_name)
          
            if "drivers_license" in file_name:
                label = "drivers_license"
            elif "bank_statement" in file_name:
                label = "bank_statement"
            elif "invoice" in file_name:
                label = "invoice"
            else:
                label = "unknown"

            texts.append(extract_text_from_pdf(file_path))
            labels.append(label)
    return texts, labels

def train_model(data_dir):
    texts, labels = load_data(data_dir)
    
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    print(classification_report(y_test, predictions))

    joblib.dump(model, '/Users/bradleyweaver/Documents/heron/join-the-siege/models/model.pkl')  




if __name__ == "__main__":
    train_model('/Users/bradleyweaver/Documents/heron/join-the-siege/files')

    