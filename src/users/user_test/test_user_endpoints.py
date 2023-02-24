import requests, os, jwt, pytest
from dotenv import load_dotenv


project_folder = os.path.expanduser("../../")
load_dotenv(os.path.join(project_folder, "global.env"))


def pytest_configure():
    pytest.TOKEN = ""


def test_env():
    assert os.environ.get("SECRET_KEY") is not None
    assert os.environ.get("TEST") == "TRUE"


def test_read_all():
    req = requests.get("http://localhost:5000/init-test")

    req = requests.get(
        "http://localhost:5000/read-users", json={}, headers={"abs": "sd"}
    )
    assert req.json() == [
        {
            "id": "22222222-b392-11ed-92c6-0242ac170004",
            "username": "test2",
            "email": "test2@gmail.com",
            "user_type": "EMPLOYER",
        },
        {
            "id": "33333333-b392-11ed-92c6-0242ac170004",
            "username": "test3",
            "email": "test3@gmail.com",
            "user_type": "ADMIN",
        },
        {
            "id": "43299a1e-b392-11ed-92c6-0242ac170004",
            "username": "test1",
            "email": "test1@gmail.com",
            "user_type": "WORKER",
        },
    ]


def test_login():
    req = requests.post(
        "http://localhost:5002/login", json={"username": "test1", "password": "123"}
    )
    pytest.TOKEN = req.json()["Bearer"]
    data = jwt.decode(pytest.TOKEN, os.environ.get("SECRET_KEY"), algorithms=["HS256"])
    assert data["username"] == "test1" and data["user_type"] == "WORKER"


def test_no_token():
    req = requests.get(
        "http://localhost:5000/read-logged-user", json={"username": "test1"}
    )
    assert req.json() == {"message": "Token is missing"}
    assert req.status_code == 401


def test_invalid_token():
    print("TOKEN")
    print(pytest.TOKEN)
    req = requests.get(
        "http://localhost:5000/read-logged-user",
        json={"username": "test1"},
        headers={"Bearer": "Invalid token"},
    )
    assert req.json() == {"message": "Token is invalid"}
    assert req.status_code == 401


def test_read_by_logged_user_valid():
    print("TOKEN")
    print(pytest.TOKEN)
    req = requests.get(
        "http://localhost:5000/read-logged-user",
        headers={"Bearer": pytest.TOKEN},
    )
    assert req.json() == {
        "id": "43299a1e-b392-11ed-92c6-0242ac170004",
        "username": "test1",
        "password": "123",
        "email": "test1@gmail.com",
        "user_type": "WORKER",
    }


def test_read_by_username_valid():
    req = requests.get(
        "http://localhost:5000/read-by-username",
        json={"username": "test1"},
    )
    assert req.json() == {
        "id": "43299a1e-b392-11ed-92c6-0242ac170004",
        "username": "test1",
        "password": None,
        "email": "test1@gmail.com",
        "user_type": "WORKER",
    }


def test_read_by_username_invalid():
    print("TOKEN")
    print(pytest.TOKEN)
    req = requests.get(
        "http://localhost:5000/read-by-username",
        json={"username": "invalid_username"},
        headers={"Bearer": pytest.TOKEN},
    )
    assert req.json() == {"message": "Invalid username"}
    assert req.status_code == 400


def test_read_by_id_valid():
    req = requests.get(
        "http://localhost:5000/read-by-id",
        json={"id": "43299a1e-b392-11ed-92c6-0242ac170004"},
    )
    assert req.json() == {
        "id": "43299a1e-b392-11ed-92c6-0242ac170004",
        "username": "test1",
        "password": None,
        "email": "test1@gmail.com",
        "user_type": "WORKER",
    }

    assert req.status_code == 200


def test_read_by_id_invalid():
    req = requests.get("http://localhost:5000/read-by-id", json={"id": "invalid"})
    assert req.json() == {"message": "Invalid user_id"}

    assert req.status_code == 400


def test_create_user_valid():
    req = requests.post(
        "http://localhost:5000/create-user",
        json={
            "username": "test4",
            "password": "123",
            "email": "test4@gmail.com",
            "user_type": "WORKER",
        },
    )
    assert req.json()["username"] == "test4"
    assert req.status_code == 201


def test_create_user_taken_username():
    req = requests.post(
        "http://localhost:5000/create-user",
        json={
            "username": "test2",
            "password": "123",
            "email": "not_taken@gmail.com",
            "user_type": "WORKER",
        },
    )
    assert "Duplicate entry 'test2' for key 'username'" in req.json()["message"]
    assert req.status_code == 400


def test_create_user_taken_email():
    req = requests.post(
        "http://localhost:5000/create-user",
        json={
            "username": "not taken",
            "password": "123",
            "email": "test1@gmail.com",
            "user_type": "WORKER",
        },
    )
    assert "Duplicate entry 'test1@gmail.com' for key 'email'" in req.json()["message"]
    assert req.status_code == 400


def test_update_user_valid():
    req = requests.put(
        "http://localhost:5000/update-user",
        json={
            "email": "test1@gmail.com",
            "id": "43299a1e-b392-11ed-92c6-0242ac170004",
            "password": "123_update",
            "user_type": "WORKER",
            "username": "test1",
        },
        headers={"Bearer": pytest.TOKEN},  # logged as test1 user
    )
    assert req.json() == {
        "email": "test1@gmail.com",
        "id": "43299a1e-b392-11ed-92c6-0242ac170004",
        "password": "123_update",
        "user_type": "WORKER",
        "username": "test1",
    }
    assert req.status_code == 201


def test_delete_user_valid():
    req = requests.delete(
        "http://localhost:5000/delete-user",
        json={"id": "43299a1e-b392-11ed-92c6-0242ac170004"},
        headers={"Bearer": pytest.TOKEN},
    )
    assert req.json() == True
    assert req.status_code == 200


def test_delete_user_invalid():
    req = requests.delete(
        "http://localhost:5000/delete-user",
        json={"id": "invalid"},
        headers={"Bearer": pytest.TOKEN},
    )
    assert req.json() == False
    assert req.status_code == 200
