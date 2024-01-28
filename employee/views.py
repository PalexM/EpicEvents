from .models import Employee as Employee
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
import click
import sentry_sdk


class EmployeeService:
    """CRUD OPERATIONS ARE HANDLED HERE"""

    @staticmethod
    def authenticate(email, password):
        try:
            user = Employee.objects.get(email=email)
            if user.check_password(password):
                sentry_sdk.capture_message(
                    f"User with email :  {email} is succefully authenticated",
                    level="info",
                )
                return True
            else:
                sentry_sdk.capture_message(
                    f"Bad email or password for user with email{email}", level="info"
                )
                return False
        except Employee.DoesNotExist as e:
            sentry_sdk.capture_exception(e)
            return False

    @staticmethod
    def register(name, email, department, password):
        try:
            if Employee.objects.filter(email=email).exists():
                sentry_sdk.capture_message(
                    f"User already exists with email: {email}", level="info"
                )
                return f"User already exists with email: {email}"

            new_user = Employee(name=name, email=email, department=department)
            new_user.set_password(password)
            new_user.save()
            sentry_sdk.capture_message(
                f"User {name} has been successfully registered.", level="info"
            )
            return f"User {name} has been successfully registered."

        except IntegrityError as e:
            sentry_sdk.capture_exception(e)
            return f"Integrity error: {e}"

        except Exception as e:
            sentry_sdk.capture_exception(e)
            return f"Unexpected error during user registration: {e}"

    @staticmethod
    def get_employee(email):
        try:
            employee = Employee.objects.get(email=email)
            sentry_sdk.capture_message(f"Getting employee ", level="info")
            return [[employee.pk, employee.name, employee.email, employee.department]]
        except ObjectDoesNotExist as e:
            sentry_sdk.capture_exception(e)
            return None

    @staticmethod
    def get_employee_object_by_email(email):
        try:
            return Employee.objects.get(email=email)
        except ObjectDoesNotExist as e:
            click.secho(f"Employee object not found with this email: {email}", fg="red")
            sentry_sdk.capture_exception(e)

    @staticmethod
    def get_employee_object_by_id(id):
        try:
            return Employee.objects.get(id=id)
        except ObjectDoesNotExist as e:
            click.secho(f"Employee object not found", fg="red")
            sentry_sdk.capture_exception(e)

    @staticmethod
    def get_employees():
        try:
            employees = Employee.objects.all()
            table = []
            for employee in employees:
                table.append(
                    [employee.pk, employee.name, employee.email, employee.department]
                )
            sentry_sdk.capture_message(f"Getting employees ", level="info")
            return table
        except ObjectDoesNotExist as e:
            sentry_sdk.capture_exception(e)
            return None

    @staticmethod
    def get_employee_id(email):
        try:
            employee = Employee.objects.get(email=email)
            sentry_sdk.capture_message(
                f"Getting employee id {employee.pk}", level="info"
            )
            return employee.pk
        except ObjectDoesNotExist as e:
            click.secho(f"Employee with email: {email} doesn't exists", fg="red")
            sentry_sdk.capture_exception(e)
