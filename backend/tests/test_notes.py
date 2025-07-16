import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import User, Note
from werkzeug.security import generate_password_hash
import mongomock
from mongoengine import connect, disconnect

@pytest.fixture(autouse=True)
def mongo_mock():
    disconnect()
    mock_client = mongomock.MongoClient(uuidRepresentation="standard")
    connect(
        db='testdb',
        alias='default',
        host='mongodb://localhost',
        mongo_client_class=lambda *args, **kwargs: mock_client
    )
    yield
    disconnect()

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def access_token(client):
    password = generate_password_hash("testpass")
    user = User(username="testuser", password=password)
    user.save()
    res = client.post('/api/login', json={"username": "testuser", "password": "testpass"})
    return res.get_json()['access_token']

def test_create_note(client, access_token):
    res = client.post('/api/notes',
        json={"title": "Test Note", "content": "Note content"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert res.status_code == 200
    assert res.get_json()["msg"] == "Note created!"

def test_get_notes(client, access_token):
    user = User.objects.first()
    Note(title="Note 1", content="Text 1", user=user).save()
    Note(title="Note 2", content="Text 2", user=user).save()

    res = client.get('/api/notes',
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data = res.get_json()
    assert res.status_code == 200
    assert len(data) == 2
    assert data[0]["title"] in ["Note 1", "Note 2"]

def test_update_note(client, access_token):
    user = User.objects.first()
    note = Note(title="Before", content="Before", user=user).save()

    res = client.put(f'/api/notes/{note.id}',
        json={"title": "After", "content": "Updated"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert res.status_code == 200
    assert res.get_json()["msg"] == "Note updated!"
    updated = Note.objects(id=note.id).first()
    assert updated.title == "After"

def test_delete_note(client, access_token):
    user = User.objects.first()
    note = Note(title="To Delete", content="Bye", user=user).save()

    res = client.delete(f'/api/notes/{note.id}',
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert res.status_code == 200
    assert res.get_json()["msg"] == "Note deleted!"
    assert Note.objects(id=note.id).first() is None

def test_search_notes(client, access_token):
    user = User.objects.first()
    # สร้างโน้ต 3 อัน (2 อันเกี่ยวกับ "Python", อีก 1 อันไม่เกี่ยว)
    Note(title="Python Tips", content="List comprehensions", user=user).save()
    Note(title="Flask Tutorial", content="Learn Flask and Python", user=user).save()
    Note(title="Shopping List", content="Eggs, Milk, Bread", user=user).save()

    # Search ด้วย keyword "python"
    res = client.get('/api/notes/search?keyword=python',
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, list)
    # ต้องเจอ 2 อันที่มีคำว่า python
    assert len(data) == 2
    titles = [note['title'] for note in data]
    assert "Python Tips" in titles
    assert "Flask Tutorial" in titles

    # Search ด้วย keyword "list"
    res = client.get('/api/notes/search?keyword=list',
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data = res.get_json()
    # ต้องเจอ 2 อัน (Python Tips กับ Shopping List)
    assert len(data) == 2
    titles = [note['title'] for note in data]
    assert "Python Tips" in titles
    assert "Shopping List" in titles

    # Search ด้วย keyword ไม่มีใน note
    res = client.get('/api/notes/search?keyword=unicorn',
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data = res.get_json()
    assert res.status_code == 200
    assert data == []