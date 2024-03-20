# python-microservice

Run tests:
cd to users/user_test
pytest -vv

venv:
source venv/bin/activate
deactivate venv
after adding new dependency
pip freeze > requirements.txt

Check metrics:
login_counter_total

Prometheus list all metrics:
{\_\_name\_\_=~".+"} WITHOUT \
