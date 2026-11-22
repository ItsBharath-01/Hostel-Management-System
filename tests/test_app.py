import pytest
from app import create_app
from app import routes


@pytest.fixture
def client():
    routes.students.clear()
    routes.next_student_id = 1

    for room in routes.rooms:
        room["students"].clear()

    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_get_rooms(client):
    response = client.get("/rooms")
    assert response.status_code == 200
    assert len(response.json["rooms"]) == 50


def test_register_student(client):
    response = client.post(
        "/students",
        json={"name": "Bharath"}
    )
    assert response.status_code == 201


def test_missing_student_name(client):
    response = client.post("/students", json={})
    assert response.status_code == 400
