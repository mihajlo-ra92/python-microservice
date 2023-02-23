import requests, os, jwt, pytest
from dotenv import load_dotenv


project_folder = os.path.expanduser("../")  # adjust as appropriate thats my directory
load_dotenv(os.path.join(project_folder, "global.env"))


def pytest_configure():
    pytest.TOKEN = ""


def test_init():
    req = requests.get(
        "http://localhost:5000/read-users", json={}, headers={"abs": "sd"}
    )
    assert req.json() == [
        {
            "id": "43299a1e-b392-11ed-92c6-0242ac170004",
            "username": "test1",
            "email": "test1@gmail.com",
            "user_type": "WORKER",
        }
    ]


def test_env():
    assert os.environ.get("SECRET_KEY") is not None
    assert os.environ.get("TEST") == "TRUE"


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


def test_by_logged_user_valid():
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
    print("TOKEN")
    print(pytest.TOKEN)
    req = requests.get(
        "http://localhost:5000/read-by-username",
        json={"username": "test1"},
        headers={"Bearer": pytest.TOKEN},
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
