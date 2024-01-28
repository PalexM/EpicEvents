from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .models import Client
from contracts.models import Contract
from employee.scripts import get_connected_employee_email
import click
import sentry_sdk


class ClientCRUD:
    """CRUD OPERATIONS ARE HANDLED HERE"""

    @staticmethod
    def create_client(full_name, email, phone, company_name, employee):
        try:
            Client.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                company_name=company_name,
                employee=employee,
            )
            click.secho(f"Client {full_name} was succesfully created", fg="green")
            sentry_sdk.capture_message(
                f"Client {full_name} was succesfully created", level="info"
            )
            return
        except IntegrityError as e:
            click.secho(f"Integrity error :  {e}", fg="red")
            sentry_sdk.capture_exception(e)
            return
        except Exception as e:
            click.secho(f"Unexpected error : {e}", fg="red")
            sentry_sdk.capture_exception(e)
            return

    @staticmethod
    def get_client(client_id):
        try:
            client = Client.objects.get(id=client_id)
            sentry_sdk.capture_message("Success getting client", level="info")
            return [
                [
                    client.id,
                    client.full_name,
                    client.email,
                    client.phone,
                    client.company_name,
                    client.date_created,
                    client.employee_id,
                    client.last_updated,
                ]
            ]
        except ObjectDoesNotExist:
            click.secho(f"Client {client_id} doesn't exists", fg="red")
            sentry_sdk.capture_exception(e)
            return False

    def get_client_object(client_id):
        try:
            Client.objects.get(id=client_id)
            sentry_sdk.capture_message("Success", level="info")
            return
        except ObjectDoesNotExist as e:
            click.secho(f"Client {client_id} doesn't exists", fg="red")
            sentry_sdk.capture_exception(e)
            return False

    @staticmethod
    def get_all_clients():
        try:
            clients = Client.objects.all()
            table = []
            for client in clients:
                table.append(
                    [
                        client.id,
                        client.full_name,
                        client.email,
                        client.phone,
                        client.company_name,
                        client.date_created,
                        client.employee,
                        client.last_updated,
                    ]
                )
            sentry_sdk.capture_message("Success getting all clients", level="info")
            return table
        except Exception as e:
            sentry_sdk.capture_exception(e)
            click.secho(f"Something went wrong, please try again", fg="red")
            return

    @staticmethod
    def update_client(client_id, **kwargs):
        try:
            client = Client.objects.get(id=client_id)
            sentry_sdk.capture_message(
                f"Client {client_id} was succesfully updated", level="info"
            )
            if has_employee_right(client.employee.email):
                for key, value in kwargs.items():
                    if value not in [None, ""]:
                        setattr(client, key, value)
                client.save()
                click.secho(
                    f"Client < {client_id} > was succesfully updated", fg="green"
                )
                return
            click.secho(
                f"You dont have rights to modify this client, please contact his manager: {client.employee.email}",
                fg="red",
            )

            return
        except Client.DoesNotExist as e:
            click.secho(f"Client < {client_id} > not found")
            sentry_sdk.capture_exception(e)
        except Exception as e:
            click.secho(
                f"Something went wrong wen we tried to update client < {client_id} , error : {e}>",
                fg="red",
            )
            sentry_sdk.capture_exception(e)
            return

    @staticmethod
    def update_client_contrat(contract_id, employee_id, **kwargs):
        try:
            contract = Contract.objects.get(id=contract_id)
            sentry_sdk.capture_message("Success", level="info")
            if contract.client.employee_id == employee_id:
                for key, value in kwargs.items():
                    if value not in [None, ""]:
                        setattr(contract, key, value)
                contract.save()
                click.secho(
                    f"Contract {contract_id} was successfully updated", fg="green"
                )
                sentry_sdk.capture_message(
                    f"Contract {contract_id} was successfully updated", level="info"
                )
                return
            else:
                click.secho(
                    f"Employee {employee_id} is not responsible for the client in Contract {contract_id}",
                    fg="red",
                )
                return

        except ObjectDoesNotExist as e:
            click.secho(f"Contract {contract_id} doesn't exist", fg="red")
            sentry_sdk.capture_exception(e)
            return
        except Exception as e:
            click.secho(f"Something went wrong: {e}", fg="red")
            sentry_sdk.capture_exception(e)
            return

    @staticmethod
    def delete_client(client_id):
        try:
            client = Client.objects.get(id=client_id)
            sentry_sdk.capture_message(f"Client {client_id} was deleted", level="info")
            if has_employee_right(client.employee.email):
                client.delete()
                click.secho(f"Client {client_id} was deleted", fg="green")
                return
            else:
                click.secho(
                    f"You dont have rights to delete this client, please contact his manager: {client.employee.email}",
                    fg="red",
                )
            return
        except ObjectDoesNotExist as e:
            click.secho(f"Client {client_id} doesn't exists", fg="red")
            sentry_sdk.capture_exception(e)
            return


def has_employee_right(client_manager_email):
    """Check if connected employee is the client manager"""
    connected_employee_email = get_connected_employee_email()
    return client_manager_email == connected_employee_email
