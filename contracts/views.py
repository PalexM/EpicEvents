from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .models import Contract
import click


class ContractCRUD:
    @staticmethod
    def create_contract(client_id, employee_id, total_amount, amount_due, status):
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
    def delete_contract(contract_id):
        try:
            contract = Contract.objects.get(id=contract_id)
            contract.delete()
            click.secho(f"Contract {contract_id} was deleted", fg="green")
            return
        except ObjectDoesNotExist:
            click.secho(f"Contract {contract_id} doesn't exists", fg="red")
            return
