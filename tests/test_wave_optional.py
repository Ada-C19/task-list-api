import pytest

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_matching_param_filtered(client, three_goals):
    # Act
    response = client.get("/goals?filter=Manage time better")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {   "id": 1,
            "title": "Manage time better"}
    ]


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_no_matching_param_filtered(client, three_goals):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {   
            "id": 1,
            "title": "Manage time better"},
        {   
            "id": 2,
            "title": "Practice self-care on a daily basis"},
        {   
            "id": 3,
            "title": "Connect with family and friends"
        }
    ]
    
