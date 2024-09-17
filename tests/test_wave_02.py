import pytest


#@pytest.mark.skip(reason="No way to test this feature yet")
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


#@pytest.mark.skip(reason="No way to test this feature yet")
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

# New test cases
#@pytest.mark.skip(reason="I created this test")
def test_get_task_filter_by_title(client, three_tasks):
    # Act
    response = client.get("/tasks?title=Answer forgotten email 📧")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "description": "",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧"},
    ]

#@pytest.mark.skip(reason="I created this test")
def test_get_task_filter_by_description(client, three_tasks_descr):
    # Act
    response = client.get("/tasks?description=%Please answer!")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "description": "Please answer!",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧"},
    ]

#@pytest.mark.skip(reason="I created this test")
def test_get_task_filter_by_id(client, three_tasks_descr):
    # Act
    response = client.get("/tasks?task_id=2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "description": "Please answer!",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧"},
    ]