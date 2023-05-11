import pytest


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_no_saved_goals(client):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


# @pytest.mark.skip(reason="No way to test this feature yet")
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


# @pytest.mark.skip(reason="No way to test this feature yet")
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


# @pytest.mark.skip(reason="test to be completed by student")
def test_get_goal_not_found(client):
    pass
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    # raise Exception("Complete test")
    # Assert
    # ---- Complete Test ----
    # assertion 1 goes here
    assert response.status_code == 404
    # assertion 2 goes here
    # assert response.get_data(as_text=True) == "Goal number 1 was not found"  
    assert response_body == {
        "details" : "Goal number 1 was not found"
    }
    # ---- Complete Test ----


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_goal(client):
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


# @pytest.mark.skip(reason="test to be completed by student")
def test_update_goal(client, one_goal):
    # raise Exception("Complete test")
    # Act
    # ---- Complete Act Here ----
    respone = client.put("/goals/1", json={
        "title": "My Updated Goal"
    })
    respone_body = respone.get_json()
    # Assert
    # ---- Complete Assertions Here ----
    # assertion 1 goes here
    assert respone.status_code == 200
    # assertion 2 goes here
    assert "goal" in respone_body
    # assertion 3 goes here
    assert respone_body == {
        "goal":{
            "id":1,
            "title": "My Updated Goal"
        }
    }
    # ---- Complete Assertions Here ----


# @pytest.mark.skip(reason="test to be completed by student")
def test_update_goal_not_found(client):
    # raise Exception("Complete test")
    # Act
    # ---- Complete Act Here ----
    respone = client.put("/goals/1")
    respone_body = respone.get_json()
    # Assert
    # ---- Complete Assertions Here ----
    # assertion 1 goes here
    assert respone.status_code == 404
    # assertion 2 goes here
    assert respone_body == {
        "details" : "Goal number 1 was not found"
    }
    # ---- Complete Assertions Here ----


# @pytest.mark.skip(reason="No way to test this feature yet")
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
    response_body = response.get_json()
    # assert response.get_data(as_text=True) == 'Goal number 1 was not found'
    assert response_body == {
        "details" : "Goal number 1 was not found"
    }
    # assert response_body == "Goal number 1 was not found" #with jsonify
    

    # raise Exception("Complete test with assertion about response body")
    # # *****************************************************************
    # # **Complete test with assertion about response body***************
    # # *****************************************************************


# @pytest.mark.skip(reason="test to be completed by student")
def test_delete_goal_not_found(client):
    # raise Exception("Complete test")

    # Act
    # ---- Complete Act Here ----
    response = client.delete("/goals/1")
    response_body = response.get_json()

    # Assert
    # ---- Complete Assertions Here ----
    # assertion 1 goes here
    assert response.status_code == 404
    # assertion 2 goes here
    assert response_body == {
        "details" : "Goal number 1 was not found"
    }
    # ---- Complete Assertions Here ----


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_goal_missing_title(client):
    # Act
    response = client.post("/goals", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }
