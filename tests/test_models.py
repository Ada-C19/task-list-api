from app.models.task import Task
import pytest


def test_to_dict_no_missing_data():
    test_data = Task(id=1,
                     title="Grocery shopping",
                     description="Buying food for the week",
                     completed_at=None)
 
    result = test_data.to_dict()

    assert type(result) == dict
    assert "task" in result
    assert result["task"]["id"] == 1
    assert result["task"]["title"] == "Grocery shopping"
    assert result["task"]["description"] == "Buying food for the week"
    assert result["task"]["is_complete"] == False


def test_to_dict_missing_title():
    test_data = Task(id=1,
                     description="Buying food for the week",
                     completed_at=None)
 
    result = test_data.to_dict()

    assert type(result) == dict
    assert "task" in result
    assert result["task"]["id"] == 1
    assert result["task"]["title"] is None
    assert result["task"]["description"] == "Buying food for the week"
    assert result["task"]["is_complete"] == False


def test_to_dict_missing_description():
    test_data = Task(id=1,
                     title="Grocery shopping",
                     completed_at=None)
 
    result = test_data.to_dict()

    assert type(result) == dict
    assert "task" in result
    assert result["task"]["id"] == 1
    assert result["task"]["title"] == "Grocery shopping"
    assert result["task"]["description"] is None
    assert result["task"]["is_complete"] == False


def test_to_dict_missing_is_complete():
    test_data = Task(id=1,
                     title="Grocery shopping",
                     description="Buying food for the week")
 
    result = test_data.to_dict()

    assert type(result) == dict
    assert "task" in result
    assert result["task"]["id"] == 1
    assert result["task"]["title"] == "Grocery shopping"
    assert result["task"]["description"] == "Buying food for the week"
    assert result["task"]["is_complete"] == False


def test_from_dict():
    test_dict = {
        "title": "Grocery shopping",
        "description": "Buying food for the week",
        "completed_at": None,
    }

    task = Task.from_dict(test_dict)

    assert task.title == "Grocery shopping"
    assert task.description == "Buying food for the week" 
    assert task.completed_at == None


def test_from_dict_missing_title():
    test_dict = {
        "description": "Buying food for the week",
        "completed_at": None,
    }

    task = Task.from_dict(test_dict)

    assert task == "Missing or invalid key 'title'"


def test_from_dict_missing_description():
    test_dict = {
        "title": "Grocery shopping",
        "completed_at": None,
    }

    task = Task.from_dict(test_dict)

    assert task == "Missing or invalid key 'description'"


def test_from_dict_missing_completed_at():
    test_dict = {
        "title": "Grocery shopping",
        "description": "Buying food for the week",
    }

    task = Task.from_dict(test_dict)

    assert task.title == "Grocery shopping"
    assert task.description == "Buying food for the week" 
    assert task.completed_at is None