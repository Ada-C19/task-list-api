def test_get_tasks_sorted_by_id_asc(client, three_tasks):
  # Act
    response = client.get("/tasks?sort=asc")
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

        { "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False},
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False}
        ]
