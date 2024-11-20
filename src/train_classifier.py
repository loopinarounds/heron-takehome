import os
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib 

# Function to extract text from PDF files
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

# Load dataset
def load_data(data_dir):
    texts = []
    labels = []
    for file_name in os.listdir(data_dir):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(data_dir, file_name)
            # You need to determine the label based on the filename or some other logic
            # For example, if the filename contains the label:
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

# Main function to train the model
def train_model(data_dir):
    # Load the data
    texts, labels = load_data(data_dir)
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

    # Create a pipeline that combines TF-IDF vectorization and Naive Bayes classification
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    
    # Train the model
    model.fit(X_train, y_train)

    # Evaluate the model
    predictions = model.predict(X_test)
    print(classification_report(y_test, predictions))

    joblib.dump(model, '/Users/bradleyweaver/Documents/heron/join-the-siege/models/model.pkl')  




if __name__ == "__main__":
    train_model('/Users/bradleyweaver/Documents/heron/join-the-siege/files')

    