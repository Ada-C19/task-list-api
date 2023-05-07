from app.models.task import Task
import pytest
import sys
sys.path.append('/Users/jessica/Ada/Unit_2/Personal_Forks/task-list-api/app')

# 200 Tests

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_no_saved_tasks_200(client):
    # Act
    response = client.get("/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_all_tasks_returns_array_of_tasks_and_200(client, three_tasks):
    response = client.get("/tasks")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response.status == "200 OK"
    assert len(response_body) == 3
    assert response_body == [
        {"id": 1, "title": "Water the garden 🌷", "description": "", "is_complete": False},
        {"id": 2, "title": "Answer forgotten email 📧", "description": "", "is_complete": False},
        {"id": 3, "title": "Pay my outstanding tickets 😭", "description": "", "is_complete": False},
    ]

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_one_saved_tasks_200(client, one_task):
    # Act
    response = client.get("/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    ]

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_task_200(client, one_task):
    # Act
    response = client.get("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    }

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_update_task_200(client, one_task):
    # Act
    response = client.put("/tasks/1", json={
        "title": "Updated Task Title",
        "description": "Updated Test Description",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Updated Task Title",
            "description": "Updated Test Description",
            "is_complete": False
        }
    }
    task = Task.query.get(1)
    assert task.title == "Updated Task Title"
    assert task.description == "Updated Test Description"
    assert task.completed_at == None

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_task_200(client, one_task):
    # Act
    response = client.delete("/tasks/1")
    response_body = response.get_json()
    print(response)
    print(response_body)
    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'
    }
    assert Task.query.get(1) == None





# 201 tests

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_task_201(client):
    # Act
    response = client.post("/tasks", json={
        "title": "A Brand New Task",
        "description": "Test Description",
    })
    response_body = response.get_json()
    print(response)
    print(response_body)
    # Assert
    assert response.status_code == 201
    assert response.status == "201 CREATED"
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "A Brand New Task",
            "description": "Test Description",
            "is_complete": False
        }
    }
    new_task = Task.query.get(1)
    assert new_task
    assert new_task.title == "A Brand New Task"
    assert new_task.description == "Test Description"
    assert new_task.completed_at == None






# Tests 400

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_task_must_contain_title_400(client):
    # Act
    response = client.post("/tasks", json={
        "description": "Test Description"
    })
    response_body = response.get_json()
    print(response)
    print(response_body)
    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Task.query.all() == []

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_task_must_contain_description_400(client):
    # Act
    response = client.post("/tasks", json={
        "title": "A Brand New Task"
    })
    response_body = response.get_json()
    print(response)
    print(response_body)
    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Task.query.all() == []

# # @pytest.mark.skip(reason="No way to test this feature yet")
# def test_create_task_must_create_completed_at_400(client):
#     # Act
#     response = client.post("/tasks", json={
#         "title": "A Brand New Task",
#         "description": "Test Description"
#     })
#     response_body = response.get_json()
#     print(response)
#     print(response_body)
#     # Assert
#     assert response.status_code == 400
#     assert "details" in response_body
#     assert response_body == {
#         "details": "Invalid data"
#     }
#     assert Task.query.all() == []

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_invalid_task_returns_400(client):
    response = client.get("/tasks/mystery")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {'message': 'Invalid task ID: mystery'}

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_update_task_not_found_400(client):
    # Act
    response = client.put("/tasks/mystery", json={
        "title": "Updated Task Title",
        "description": "Updated Test Description",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {'message': 'Invalid task ID: mystery'}

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_task_not_found_400(client):
    # Act
    response = client.delete("/tasks/mystery")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert Task.query.all() == []
    assert response_body == {'message': 'Invalid task ID: mystery'}






# 404 tests

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_task_not_found_404(client):
    # Act
    response = client.get("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

    # raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************
    assert response_body == {'message': 'Task 1 was not found.'}

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_update_task_not_found_404(client):
    # Act
    response = client.put("/tasks/1", json={
        "title": "Updated Task Title",
        "description": "Updated Test Description",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

    # raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************
    assert response_body == {'message': 'Task 1 was not found.'}

    # @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_task_not_found_404(client):
    # Act
    response = client.delete("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert Task.query.all() == []

    # raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************
    assert response_body == {'message': 'Task 1 was not found.'}