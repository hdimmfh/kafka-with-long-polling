import json

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_produce():
    response = client.get('/produce/test_message')
    assert response.status_code == 200
    assert json.loads(str(response.content, 'utf-8'))['content'] == 'succeed'
    return json.loads(str(response.content, 'utf-8'))['content']


def test_consume():
    response = client.get('/consume')
    assert response.status_code == 408
    return json.loads(str(response.content, 'utf-8'))['content'] == 'error'
