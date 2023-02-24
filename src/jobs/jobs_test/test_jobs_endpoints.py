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
            "completed": 0,
        },
        {
            "id": "job3",
            "employer_id": "employer2",
            "worker_id": "worker1",
            "job_name": "name3",
            "job_desc": "desc3",
            "pay_in_euro": 3.0,
            "completed": 1,
        },
        {
            "id": "job4",
            "employer_id": "employer2",
            "worker_id": "worker2",
            "job_name": "name4",
            "job_desc": "desc4",
            "pay_in_euro": 4.0,
            "completed": 1,
        },
        {
            "id": "job5",
            "employer_id": "employer1",
            "worker_id": None,
            "job_name": "name5",
            "job_desc": "desc5",
            "pay_in_euro": 5.0,
            "completed": 0,
        },
    ]


# def test_login():
#     req = requests.post(
#         "http://localhost:5002/login", json={"username": "test1", "password": "123"}
#     )
#     pytest.TOKEN = req.json()["Bearer"]
#     data = jwt.decode(pytest.TOKEN, os.environ.get("SECRET_KEY"), algorithms=["HS256"])
#     assert data["username"] == "test1" and data["user_type"] == "WORKER"


def test_read_by_id_valid():
    req = requests.get("http://localhost:5001/read-by-id", json={"id": "job1"})
    assert req.json() == "not implemented"
