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
    req = requests.get("http://app.localhost/jobs/init-test")

    req = requests.get(
        "http://app.localhost/jobs/read-all", json={}, headers={"abs": "sd"}
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


def test_read_by_id_valid():
    req = requests.get("http://app.localhost/jobs/read-by-id", json={"id": "job1"})
    assert req.json() == {
        "id": "job1",
        "employer_id": "employer1",
        "worker_id": "worker1",
        "job_name": "name1",
        "job_desc": "desc1",
        "pay_in_euro": 1.0,
        "completed": 1,
    }


def test_read_by_id_invalid():
    req = requests.get("http://app.localhost/jobs/read-by-id", json={"id": "invalid"})
    assert req.json() == {"message": "Invalid job_id"}


def test_create_job_valid():
    req = requests.post(
        "http://app.localhost/jobs/create",
        json={
            "id": "job6",
            "employer_id": "employer1",
            "worker_id": "worker1",
            "job_name": "name1",
            "job_desc": "desc1",
            "pay_in_euro": 1.0,
            "completed": 0,
        },
    )
    assert req.json()["employer_id"] == "employer1"


def test_create_job_invalid():
    req = requests.post(
        "http://app.localhost/jobs/create",
        json={
            "id": "job6",
            "employer_id": "employer1",
            # "worker_id" :"worker1,"
            "job_name": "name1",
            "job_desc": "desc1",
            "pay_in_euro": 1.0,
            "completed": 0,
        },
    )
    assert req.json()["message"] == "Please send all job data"


def test_create_job_worker():
    req = requests.post(
        "http://app.localhost/jobs/create",
        json={
            "id": "job6",
            "employer_id": "worker1",
            "worker_id": "worker2",
            "job_name": "name1",
            "job_desc": "desc1",
            "pay_in_euro": 1.0,
            "completed": 0,
        },
    )
    assert req.json()["message"] == "Sent employer_id must be of an employer"


def test_create_job_invalid_employer_id():
    req = requests.post(
        "http://app.localhost/jobs/create",
        json={
            "id": "job6",
            "employer_id": "invalid",
            "worker_id": "worker2",
            "job_name": "name1",
            "job_desc": "desc1",
            "pay_in_euro": 1.0,
            "completed": 0,
        },
    )
    assert req.json()["message"] == "Sent employer_id not valid"


def test_update_job_valid():
    req = requests.put(
        "http://app.localhost/jobs/update",
        json={
            "id": "job1",
            "employer_id": "employer1",
            "worker_id": "worker1",
            "job_name": "name1",
            "job_desc": "desc1",
            "pay_in_euro": 1.0,
            "completed": 1,
        },
    )

    assert req.json() == {
        "id": "job1",
        "employer_id": "employer1",
        "worker_id": "worker1",
        "job_name": "name1",
        "job_desc": "desc1",
        "pay_in_euro": 1.0,
        "completed": 1,
    }


def test_delete_user_valid():
    req = requests.delete(
        "http://app.localhost/jobs/delete",
        json={"id": "job1"},
    )
    assert req.json() == True
    assert req.status_code == 200


def test_delete_user_invalid():
    req = requests.delete(
        "http://app.localhost/jobs/delete",
        json={"id": "invalid"},
    )
    assert req.json() == False
    assert req.status_code == 200
