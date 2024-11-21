import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from data_loader import load_data 
from collections import Counter


import os

def train_model(data_dir):
    
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"The directory {data_dir} does not exist.")


    texts, labels = load_data(data_dir)
   
    if not texts or not labels:
        raise ValueError("No data loaded. Please check the data directory and ensure it contains valid data.")
    
    class_distribution = Counter(labels)
    print("Class distribution:", class_distribution)  
    
    insufficient_classes = [label for label, count in class_distribution.items() if count < 2]
    if insufficient_classes:
        print(f"Classes with insufficient samples: {insufficient_classes}")
        
        texts = [text for text, label in zip(texts, labels) if label not in insufficient_classes]
        labels = [label for label in labels if label not in insufficient_classes]
        
    num_classes = len(set(labels))

    test_size = max(0.2, num_classes / len(labels))  


    if test_size * len(labels) < num_classes:
        test_size = num_classes / len(labels)  
    
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=test_size, random_state=42, stratify=labels)
    
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(X_train, y_train)
    
    

    predictions = model.predict(X_test)
    print(classification_report(y_test, predictions))

  
    model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')  
    if not os.path.exists(model_dir):
        os.makedirs(model_dir) 
        
    joblib.dump(model, os.path.join(model_dir, 'model.pkl'))  

if __name__ == "__main__":
    train_model(os.path.join(os.path.dirname(__file__), '../files')) 