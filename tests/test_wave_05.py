import pytest
from app.models.goal import Goal
from app import db


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_no_saved_goals_200(client):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_one_saved_goal_200(client, one_goal):
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

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goal_200(client, one_goal):
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

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_goal_200(client, one_goal):
    # Act
    response = client.delete("/goals/1")
    response_body = response.get_json()
    print(f"{response = }")
    print(f"{response_body = }")
    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Goal 1 "Build a habit of going outside daily" successfully deleted'
    }

    # Check that the goal was deleted
    response = client.get("/goals/1")
    assert response.status_code == 404
    assert db.session.get(Goal, 1) is None

# @pytest.mark.skip(reason="test to be completed by student")
def test_update_goal_200(client, one_goal):
    # Act
    response = client.put("/goals/1", json={
        "title": "Updated goal Title",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "Updated goal Title"
        }
    }
    goal = db.session.get(Goal, 1)
    assert goal.title == 'Updated goal Title'






# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_goal_201(client):
    # Act
    response = client.post("/goals", json={
        "title": "My New Goal"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "My New Goal"
        }
    }



# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_goal_missing_title_400(client):
    # Act
    response = client.post("/goals", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }





# @pytest.mark.skip(reason="test to be completed by student")
def test_get_goal_not_found_404(client):
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body["message"] == 'Goal 1 was not found.'

# @pytest.mark.skip(reason="test to be completed by student")
def test_delete_goal_not_found_404(client):
    # Act
    response = client.delete("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert Goal.query.all() == []
    assert response_body == {'message': 'Goal 1 was not found.'}

# @pytest.mark.skip(reason="test to be completed by student")
def test_update_goal_not_found_404(client):
    # Act
    response = client.put("/goals/1", json={
        "title": "Updated Goal Title",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {'message': 'Goal 1 was not found.'}






