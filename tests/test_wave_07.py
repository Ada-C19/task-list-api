import pytest

def test_get_tasks_order_id_sorted_asc(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=asc&order_by=id")
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

def test_get_tasks_sort_desc_invalid_order_param_defaults_to_title(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=desc&order_by=surprise")
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
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False},
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False}
    ]

def test_get_tasks_filter_title_substring(client, three_tasks):
    # Act
    response = client.get("/tasks?title=te")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
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
            "is_complete": False}
    ]

def test_get_tasks_filter_title_substring_orderby_id_sort_desc(client, three_tasks):
    # Act
    response = client.get("/tasks?title=te&sort=desc&order_by=id")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [     
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False},
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False}
    ]