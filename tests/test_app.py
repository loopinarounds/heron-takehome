from io import BytesIO
import pytest
from src.app import app, allowed_file

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.mark.parametrize("filename, expected", [
    ("file.pdf", True),
    ("file.png", True),
    ("file.jpg", True),
    ("file.docx", True),
    ("file.txt", False),
    ("file", False),
])


def test_allowed_file(filename, expected):
    assert allowed_file(filename) == expected

def test_no_file_in_request(client):
    response = client.post('/classify_file')
    assert response.status_code == 400
    assert response.get_json() == {"error": "No file in the request"}

def test_no_selected_file(client):
    data = {'file': (BytesIO(b""), '')}  # Empty filename
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.get_json() == {"error": "No selected files"}

def test_success(client, mocker):
    mocker.patch('src.app.predict_file_class', return_value='test_class')

    data = {'file': (BytesIO(b"dummy content"), 'file.pdf')}
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.get_json() == [{"filename": "file.pdf", "file_class": "test_class"}]

def test_multiple_files_success(client, mocker):
    mocker.patch('src.app.predict_file_class', side_effect=['class1', 'class2'])

    data = {
        'file': [
            (BytesIO(b"dummy content 1"), 'file1.pdf'),
            (BytesIO(b"dummy content 2"), 'file2.docx')
        ]
    }
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.get_json() == [
        {"filename": "file1.pdf", "file_class": "class1"},
        {"filename": "file2.docx", "file_class": "class2"}
    ]

def test_unsupported_file_type(client):
    data = {'file': (BytesIO(b"dummy content"), 'file.txt')}
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.get_json() == [{"filename": "file.txt", "error": "Unsupported file type"}]
