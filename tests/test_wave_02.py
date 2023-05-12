import pytest


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_sorted_asc(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False},
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False},
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False}
    ]


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_sorted_desc(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=desc")
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
            "id": 3,
            "is_complete": False,
            "title": "Pay my outstanding tickets 😭"},
        {
            "description": "",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧"},
    ]


def test_get_tasks_sorted_asc_by_description(client, three_tasks_with_description):
    # Act
    response = client.get("/tasks?sort=description_asc")
    response_body = response.get_json()
    print(f"{response_body = }")
    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "1",
            "is_complete": False},
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "2",
            "is_complete": False},
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "3",
            "is_complete": False}
    ]


def test_get_tasks_sorted_desc_by_description(client, three_tasks_with_description):
    # Act
    response = client.get("/tasks?sort=description_desc")
    response_body = response.get_json()
    print(f"{response_body = }")
    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "3",
            "is_complete": False},
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "2",
            "is_complete": False},
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "1",
            "is_complete": False}
    ]

