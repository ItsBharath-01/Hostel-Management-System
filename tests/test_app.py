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


def test_room_numbers(client):
    response = client.get("/rooms")
    room_list = response.json["rooms"]

    assert room_list[0]["room_id"] == 101
    assert room_list[-1]["room_id"] == 150

def test_hostel_statistics_empty(client):
    response = client.get("/hostel/statistics")

    assert response.status_code == 200
    assert response.json["total_rooms"] == 50
    assert response.json["occupied_rooms"] == 0
    assert response.json["available_rooms"] == 50
    assert response.json["total_beds"] == 100
    assert response.json["occupied_beds"] == 0
    assert response.json["available_beds"] == 100
    assert response.json["occupancy_percentage"] == 0


def test_hostel_statistics_after_allocation(client):
    student_response = client.post(
        "/students",
        json={"name": "Bharath"}
    )

    student_id = student_response.json["student"]["student_id"]

    allocation_response = client.post(
        "/allocate",
        json={
            "student_id": student_id,
            "room_id": 101
        }
    )

    assert allocation_response.status_code == 200

    response = client.get("/hostel/statistics")

    assert response.status_code == 200
    assert response.json["occupied_rooms"] == 1
    assert response.json["available_rooms"] == 49
    assert response.json["occupied_beds"] == 1
    assert response.json["available_beds"] == 99
    assert response.json["occupancy_percentage"] == 1.0
