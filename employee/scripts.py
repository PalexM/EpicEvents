import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EpicEvents.settings")
django.setup()
import jwt
import json
from django.core.exceptions import ObjectDoesNotExist

import datetime
from employee.views import EmployeeService
import sentry_sdk


def is_token_valid():
    secret = get_secret()
    try:
        with open(f"secrets/employee_token.json", "r") as file:
            data = json.load(file)
            token = data["token"]
            jwt.decode(token, secret, algorithms=["HS256"])
            return True
    except (FileNotFoundError, jwt.ExpiredSignatureError, jwt.DecodeError) as e:
        sentry_sdk.capture_exception(e)
        return False


def check_json_file():
    try:
        with open("secrets/employee_token.json", "r") as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        sentry_sdk.capture_exception(e)
        return False

    if "token" in data:
        return is_token_valid()
    else:
        return False


def generate_token(email):
    secret = get_secret()

    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    token = jwt.encode(
        {"email": email, "exp": expiration_time}, secret, algorithm="HS256"
    )
    data = {"token": token, "email": email}

    with open("secrets/employee_token.json", "w") as file:
        json.dump(data, file)
    return


def get_secret():
    with open(f"secrets/secret.json", "r") as file:
        data = json.load(file)
        secret = data["secret"]
        return secret


def get_connected_employee_email():
    try:
        with open("secrets/employee_token.json", "r") as file:
            data = json.load(file)
            email = data["email"]
            sentry_sdk.capture_message(f"Getting email :  {email}", level="info")
            return email
    except json.JSONDecodeError as e:
        sentry_sdk.capture_exception(e)
        return False


def get_role():
    try:
        with open("secrets/employee_token.json", "r") as file:
            data = json.load(file)
            email = data["email"]
            employee = EmployeeService.get_employee_object_by_email(email)
            sentry_sdk.capture_message(f"Getting role for {email}", level="info")
            return employee.department
    except json.JSONDecodeError as e:
        sentry_sdk.capture_exception(e)
        return False
