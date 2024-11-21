
## Getting Started
1. Clone the repository:
    ```shell
    git clone <repository_url>
    cd heron_classifier
    ```

2. Install dependencies:
    ```shell
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Run the Flask app:
    ```shell
    python -m src.app
    ```

4. Train the model based on the files found in '/files':
```shell 
    python -m src/train_classifier
    ```

5. Test the classifier using a tool like curl:
    ```shell
    curl -X POST -F 'file=@path_to_pdf.pdf' http://127.0.0.1:5000/classify_file
    ```
    Multiple files are accepted: 
    ```shell
    curl -X POST \
-F 'file=@/file_path' \
-F 'file=@/file_path' \
http://127.0.0.1:5000/classify_file```

5. Run tests:
   ```shell
    pytest
    ```

