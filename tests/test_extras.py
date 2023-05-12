import pytest
from app.models.task import Task

def test_get_goals_sorted_asc(client, three_goals):
    # Act
    response = client.get("/goals?sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 3,
            "title": "Go on a walk daily"},
        {
            "id": 1,
            "title": "Learn how to swim"},
        {
            "id": 2,
            "title": "Play all the major scales on piano"},
    ]


def test_get_goals_sorted_desc(client, three_goals):
    # Act
    response = client.get("/goals?sort=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 2,
            "title": "Play all the major scales on piano"},
        {
            "id": 1,
            "title": "Learn how to swim"},
        {
            "id": 3,
            "title": "Go on a walk daily"},
    ]


def test_get_goals_sorted_asc_by_id_as_default(client, three_goals):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 1,
            "title": "Learn how to swim"},
        {
            "id": 2,
            "title": "Play all the major scales on piano"},
        {
            "id": 3,
            "title": "Go on a walk daily"},
    ]


def test_get_tasks_sorted_asc_by_id_as_default(client, three_tasks):
    # Act
    response = client.get("/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "description": "",
            "id": 1,
            "is_complete": False,
            "title": "Water the garden 🌷"},
        {
            "description": "",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧"},
        {
            "description": "",
            "id": 3,
            "is_complete": False,
            "title": "Pay my outstanding tickets 😭"},
    ]

# @pytest.mark.skip
def test_create_task_with_invalid_completed_at(client):
    response = client.post("/tasks", json={
        "title": "A Brand New Task",
        "description": "Test Description",
        "completed_at": "Time Completed"
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Task.query.all() == []


def test_update_task_invalid_completed_at(client, one_task):
    response = client.put("/tasks/1", json={
        "title": "Updated Task Title",
        "description": "Updated Test Description",
        "completed_at": "Updated Completed At"
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }