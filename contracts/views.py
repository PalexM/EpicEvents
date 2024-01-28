from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .models import Contract
from employee.models import Employee
from employee.scripts import get_role
from django.core.exceptions import FieldError
import click
import sentry_sdk


class ContractCRUD:
    """CRUD OPERATIONS ARE HANDLED HERE"""

    @staticmethod
    def create_contract(client_id, employee_id, total_amount, amount_due, status):
        if is_designed_salesman_part_of_sales_team(employee_id):
            try:
                Contract.objects.create(
                    client_id=client_id,
                    employee_id=employee_id,
                    total_amount=total_amount,
                    amount_due=amount_due,
                    status=status,
                )

                click.secho(f"Ccontract was succesfully created", fg="green")
                sentry_sdk.capture_message(
                    "Ccontract was succesfully created", level="info"
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
        else:
            click.secho(f"The designated employee is not part of Sales team", fg="red")
            return

    @staticmethod
    def get_contract(contract_id):
        try:
            contract = Contract.objects.get(id=contract_id)
            sentry_sdk.capture_message(
                f"Success getting contract {contract_id}", level="info"
            )
            return [
                [
                    contract.pk,
                    contract.total_amount,
                    contract.amount_due,
                    contract.creation_date,
                    contract.status,
                    contract.client,
                    contract.employee,
                ]
            ]
        except ObjectDoesNotExist as e:
            click.secho(f"Contract {contract_id} doesn't exists", fg="red")
            sentry_sdk.capture_exception(e)
            return False

    @staticmethod
    def get_contracts():
        try:
            contracts = Contract.objects.all()
            sentry_sdk.capture_message("Success getting all contracts", level="info")
            table = []
            for contract in contracts:
                table.append(
                    [
                        contract.pk,
                        contract.total_amount,
                        contract.amount_due,
                        contract.creation_date,
                        contract.status,
                        contract.client,
                        contract.employee,
                    ]
                )
            return table

        except Exception as e:
            click.secho(f"Something went wrong : {e} ", fg="red")
            sentry_sdk.capture_exception(e)
            return

    @staticmethod
    def update_contract(contract_id, **kwargs):
        try:
            contract = Contract.objects.get(id=contract_id)
            sentry_sdk.capture_message(
                f"Contract {contract_id} was succesfully updated", level="info"
            )
            for key, value in kwargs.items():
                if value not in [None, ""]:
                    setattr(contract, key, value)
            contract.save()
            click.secho(f"Contract {contract_id} was succesfully updated", fg="green")
            return
        except ObjectDoesNotExist as e:
            click.secho(f"Contract {contract_id} doesn't exists", fg="red")
            sentry_sdk.capture_exception(e)
            return

    @staticmethod
    def filter_contracts(filter_criteria):
        try:
            contracts = Contract.objects.filter(**filter_criteria)
            sentry_sdk.capture_message("Success filtering contracts", level="info")
            table = []
            for contract in contracts:
                table.append(
                    [
                        contract.pk,
                        contract.total_amount,
                        contract.amount_due,
                        contract.creation_date,
                        contract.status,
                        contract.client,
                        contract.employee,
                    ]
                )
            return table
        except FieldError as e:
            click.secho(f"Filter Error: {e}", fg="red")
            sentry_sdk.capture_exception(e)
            return
        except Exception as e:
            click.secho(f"Something went wrong: {e}", fg="red")
            sentry_sdk.capture_exception(e)
            return

    @staticmethod
    def delete_contract(contract_id):
        try:
            contract = Contract.objects.get(id=contract_id)
            contract.delete()
            click.secho(f"Contract {contract_id} was deleted", fg="green")
            sentry_sdk.capture_message(
                f"Contract {contract_id} was deleted", level="info"
            )
            return
        except ObjectDoesNotExist as e:
            click.secho(f"Contract {contract_id} doesn't exists", fg="red")
            sentry_sdk.capture_exception(e)
            return


def is_designed_salesman_part_of_sales_team(employee_id):
    employee = Employee.objects.get(id=employee_id)
    return employee.department == "Sales"
