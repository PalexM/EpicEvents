from .models import Employee as Employee
from django.core.exceptions import ObjectDoesNotExist
import click


class EmployeeService:
    @staticmethod
    def authenticate(email, password):
        try:
            user = Employee.objects.get(email=email)
            if user.check_password(password):
                return True
            else:
                return False
        except Employee.DoesNotExist:
            return False

    @staticmethod
    def register(name, email, department, password):
        if Employee.objects.filter(email=email).exists():
            return f"Încercare de înregistrare eșuată, email existent: {email}"

        new_user = Employee(name=name, email=email, department=department)
        new_user.set_password(password)
        new_user.save()
        return f"Utilizatorul {name} a fost înregistrat cu succes."

    @staticmethod
    def get_employee(email):
        try:
            employee = Employee.objects.get(email=email)
            return [[employee.pk, employee.name, employee.email, employee.department]]
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_employee_object_by_email(email):
        try:
            return Employee.objects.get(email=email)
        except ObjectDoesNotExist:
            click.secho(f"Employee object not found with this email: {email}", fg="red")

    @staticmethod
    def get_employee_object_by_id(id):
        try:
            return Employee.objects.get(id=id)
        except ObjectDoesNotExist:
            click.secho(f"Employee object not found", fg="red")

    @staticmethod
    def get_employees():
        try:
            employees = Employee.objects.all()
            table = []
            for employee in employees:
                table.append(
                    [employee.pk, employee.name, employee.email, employee.department]
                )
            return table
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_employee_id(email):
        try:
            employee = Employee.objects.get(email=email)
            return employee.pk
        except ObjectDoesNotExist:
            click.secho(f"Employee with email: {email} doesn't exists", fg="red")
