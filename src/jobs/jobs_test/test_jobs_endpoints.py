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
    req = requests.get("http://localhost:5001/init-test")

    req = requests.get(
        "http://localhost:5001/read-jobs", json={}, headers={"abs": "sd"}
    )
    assert req.json() == [
        {
            "id": "job1",
            "employer_id": "employer1",
            "worker_id": "worker1",
            "job_name": "name1",
            "job_desc": "desc1",
            "pay_in_euro": 1.0,
            "completed": 1,
        },
        {
            "id": "job2",
            "employer_id": "employer1",
            "worker_id": "worker2",
            "job_name": "name2",
            "job_desc": "desc2",
            "pay_in_euro": 2.0,
            "completed": 1,
        },
    ]
