# Task List API

## Skills Assessed

- Reading, writing, and using tests
- Demonstrating understanding of the client-server model, request-response cycle and conventional RESTful routes
- Driving development with independent research, experimentation, and collaboration
- Reading and using existing external web APIs
- Using Postman as part of the development workflow


Working with the Flask package:

- Creating models
- Creating conventional RESTful CRUD routes for a model
- Reading query parameters to create custom behavior
- Create unconventional routes for custom behavior
- Apply knowledge about making requests in Python, to call an API inside of an API
- Apply knowledge about environment variables
- Creating a one-to-many relationship between two models

## Goals

There's so much we want to do in the world! When we organize our goals into smaller, bite-sized tasks, we'll be able to track them more easily, and complete them!

If we make a web API to organize our tasks, we'll be able to create, read, update, and delete tasks as long as we have access to the Internet and our API is running!

We also want to do some interesting features with our tasks. We want to be able to:

- Sort tasks
- Mark them as complete
- Get feedback about our task list through Slack
- Organize tasks with goals

... and more!

# Requirements

- Python 
- Flask
- pip
- SQLAlchemy


## Fork and Clone

1. Fork this project repo to your own personal account
1. Clone this new forked project

## Managing Dependencies

Create a virtual environment:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ # You're in activated virtual environment!
```

Install dependencies (we've already gathered them all into a `requirements.txt` file):

```bash
(venv) $ pip install -r requirements.txt
```

## Setting Up Development and Test Databases

Create two databases:

1. A development database named `task_list_api_development`
1. A test database named `task_list_api_test`

## Creating a `.env` File

Create a file named `.env`.

Create two environment variables that will hold your database URLs.

1. `SQLALCHEMY_DATABASE_URI` to hold the path to your development database
1. `SQLALCHEMY_TEST_DATABASE_URI` to hold the path to your development database

Your `.env` may look like this:

```
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/task_list_api_development
SQLALCHEMY_TEST_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/task_list_api_test
```

## Run `$ flask db init`

Run `$ flask db init`.

**_After you make your first model in Wave 1_**, run the other commands `migrate` and `upgrade`.

## Run `$ flask run` or `$ FLASK_ENV=development flask run`

Check that your Flask server can run with `$ flask run`.

We can run the Flask server specifying that we're working in the development environment. This enables hot-reloading, which is a feature that refreshes the Flask server every time there is a detected change.

```bash
$ FLASK_ENV=development flask run
```

**It is highly recommended to run the Flask servers with this command**.


## Project Directions

This project is designed to fulfill the features described in detail in each wave. The tests are meant to only guide your development.

1. [Testing](ada-project-docs/testing.md)
1. [Wave 1: CRUD for one model](ada-project-docs/wave_01.md)
1. [Wave 2: Using query params](ada-project-docs/wave_02.md)
1. [Wave 3: Creating custom endpoints](ada-project-docs/wave_03.md)
1. [Wave 4: Using an external web API](ada-project-docs/wave_04.md)
1. [Wave 5: Creating a second model](ada-project-docs/wave_05.md)
1. [Wave 6: Establishing a one-to-many relationship between two models](ada-project-docs/wave_06.md)
1. [Wave 7: Deployment](ada-project-docs/wave_07.md)
1. [Optional Enhancements](ada-project-docs/optional-enhancements.md)
