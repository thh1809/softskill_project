import pytest
from app.main import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_courses(client):
    response = client.get('/api/courses/')
    assert response.status_code == 200
    assert isinstance(response.json, list)