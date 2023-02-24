import requests, os, jwt, pytest
from dotenv import load_dotenv


project_folder = os.path.expanduser("../../")
load_dotenv(os.path.join(project_folder, "global.env"))


def pytest_configure():
    pytest.TOKEN = ""


def test_env():
    assert os.environ.get("SECRET_KEY") is not None
    assert os.environ.get("TEST") == "TRUE"


def test_init():
    req = requests.get("http://localhost:5001/init-test")

    req = requests.get(
        "http://localhost:5001/read-jobs", json={}, headers={"abs": "sd"}
    )
    assert req.json() == [
        {
            "id": "43299a1e-b392-11ed-92c6-0242ac170004",
            "username": "test1",
            "email": "test1@gmail.com",
            "user_type": "WORKER",
        }
    ]
