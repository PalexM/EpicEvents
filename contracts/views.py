from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .models import Contract
from employee.models import Employee
from employee.scripts import get_role
from django.core.exceptions import FieldError
import click


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

                click.secho(f"Contrat succesfully created", fg="green")
                return
            except IntegrityError as e:
                click.secho(f"Integrity error :  {e}", fg="red")
                return
            except Exception as e:
                click.secho(f"Unexpected error : {e}", fg="red")
                return
        else:
            click.secho(f"The designated employee is not part of Sales team", fg="red")
            return

    @staticmethod
    def get_contract(contract_id):
        try:
            contract = Contract.objects.get(id=contract_id)
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
        except ObjectDoesNotExist:
            click.secho(f"Contract {contract_id} doesn't exists", fg="red")
            return False

    @staticmethod
    def get_contracts():
        try:
            contracts = Contract.objects.all()

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
            return

    @staticmethod
    def update_contract(contract_id, **kwargs):
        try:
            contract = Contract.objects.get(id=contract_id)
            for key, value in kwargs.items():
                if value not in [None, ""]:
                    setattr(contract, key, value)
            contract.save()
            click.secho(f"Contract {contract_id} was succesfully updated", fg="green")
            return
        except ObjectDoesNotExist:
            click.secho(f"Contract {contract_id} doesn't exists", fg="red")
            return

    @staticmethod
    def filter_contracts(filter_criteria):
        try:
            contracts = Contract.objects.filter(**filter_criteria)
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
            return
        except Exception as e:
            click.secho(f"Something went wrong: {e}", fg="red")
            return

    @staticmethod
    def delete_contract(contract_id):
        try:
            contract = Contract.objects.get(id=contract_id)
            contract.delete()
            click.secho(f"Contract {contract_id} was deleted", fg="green")
            return
        except ObjectDoesNotExist:
            click.secho(f"Contract {contract_id} doesn't exists", fg="red")
            return


def is_designed_salesman_part_of_sales_team(employee_id):
    employee = Employee.objects.get(id=employee_id)
    return employee.department == "Sales"
