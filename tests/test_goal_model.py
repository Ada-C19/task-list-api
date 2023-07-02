from app.models.goal import Goal
import pytest


def test_goal_to_dict_no_missing_data():
    test_data = Goal(id=1,
                     title="Eat more fruits and veggies")
 
    result = test_data.to_dict()

    assert type(result) == dict
    assert "goal" in result
    assert result["goal"]["id"] == 1
    assert result["goal"]["title"] == "Eat more fruits and veggies"


def test_goal_to_dict_missing_title():
    test_data = Goal(id=1)
 
    result = test_data.to_dict()

    assert type(result) == dict
    assert "goal" in result
    assert result["goal"]["id"] == 1
    assert result["goal"]["title"] is None


def test_goal_from_dict():
    test_dict = {
        "title": "Eat more fruits and veggies",
    }

    goal = Goal.from_dict(test_dict)

    assert goal.title == "Eat more fruits and veggies"


def test_goal_from_dict_missing_title():
    test_dict = {}

    goal = Goal.from_dict(test_dict)

    assert goal == "Missing key 'title'"
