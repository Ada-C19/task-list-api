def test_get_tasks_sorted_asc_with_id_in_param(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=asc&sort_by=id")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False},
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False},
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False}
    ]

def test_get_tasks_sorted_desc_with_id_in_param(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=desc&sort_by=id")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
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
        {
            "description": "",
            "id": 1,
            "is_complete": False,
            "title": "Water the garden 🌷"}
        
    ]

def test_get_tasks_sorted_asc_with_title_in_param(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=asc&sort_by=title")
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

def test_get_tasks_sorted_desc_with_title_in_param(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=desc&sort_by=title")
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

def test_get_tasks_sorted_incorrect_sort(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=blah&sort_by=title")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"details": "sort must be ascending or descending"}

def test_get_tasks_sorted_incorrect_sort_key(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=desc&sort_by=blah")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"details": "sort type is not accepted"}
