import pytest

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