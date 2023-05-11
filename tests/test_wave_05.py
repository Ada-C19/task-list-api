import pytest


pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_no_saved_goals(client):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_one_saved_goal(client, one_goal):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Build a habit of going outside daily"
        }
    ]


pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goal(client, one_goal):
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "Build a habit of going outside daily"
        }
    }


pytest.mark.skip(reason="test to be completed by student")
def test_get_goal_not_found(client):
    
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    # raise Exception("Complete test")
    # Assert
    assert response.status_code == 404
    assert "details" in response_body
    assert response_body["details"] == "Goal not found"


def test_create_goal(client):
    # Act
    response = client.post("/goals", json={
        "title": "My New Goal"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "goal" in response_body
    assert response_body["goal"]["id"] is not None  # Check if goal_id is not None
    assert response_body == {
        "goal": {
            "id": response_body["goal"]["id"],  # Use the assigned goal_id
            "title": "My New Goal"
        }
    }


pytest.mark.skip(reason="test to be completed by student")
def test_update_goal(client, one_goal):
    goal_id = one_goal.goal_id

    # Act
    response = client.put(f"/goals/{goal_id}", json={
    "title": "Updated Goal Title",
    "description": "Updated Goal Description"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "goal" in response_body
    assert response_body["goal"]["goal_id"] == goal_id
    assert response_body["goal"]["title"] == "Updated Goal Title"
    assert response_body["goal"]["description"] == "Updated Goal Description"



pytest.mark.skip(reason="test to be completed by student")
def test_update_goal_not_found(client):
    # Act
    response = client.put('/goals/999', json={
    "title": "Update Goal Title",
    "description": "Update Goal Description"
})

    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"details": "Goal not found"}



pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_goal(client, one_goal):
    # Act
    response = client.delete("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Goal 1 "Build a habit of going outside daily" successfully deleted'
    }

    # Check that the goal was deleted
    response = client.get("/goals/1")
    assert response.status_code == 404

    # raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************


pytest.mark.skip(reason="test to be completed by student")
def test_delete_goal_not_found(client):
    # raise Exception("Complete test")

    # Act
    response = client.delete("/goals/1")
    response_body = response.get_json()

    # Assert
    # ---- Complete Assertions Here ----
    assert response.status_code == 404
    assert response_body == {"details": "Goal not found"}
    
    # assertion 2 goes here
    # ---- Complete Assertions Here ----


pytest.mark.skip(reason="No way to test this feature yet")
def test_create_goal_missing_title(client):
    # Act
    response = client.post("/goals", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }
