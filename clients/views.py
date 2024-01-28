from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .models import Client
import click


class ClientCRUD:
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
            return
        except IntegrityError as e:
            click.secho(f"Integrity error :  {e}", fg="red")
            return
        except Exception as e:
            click.secho(f"Unexpected error : {e}", fg="red")
            return

    @staticmethod
    def get_client(client_id):
        try:
            client = Client.objects.get(id=client_id)
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
            return False

    def get_client_object(client_id):
        try:
            return Client.objects.get(id=client_id)
        except ObjectDoesNotExist:
            click.secho(f"Client {client_id} doesn't exists", fg="red")
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
                        client.employee_id,
                        client.last_updated,
                    ]
                )
            return table
        except:
            click.secho(f"Something went wrong, please try again", fg="red")
            return

    @staticmethod
    def update_client(client_id, **kwargs):
        try:
            client = Client.objects.get(id=client_id)
            for key, value in kwargs.items():
                # Verifică dacă valoarea este diferită de un șir gol sau None
                if value not in [None, ""]:
                    setattr(client, key, value)

            client.save()  # Deblocată pentru a salva modificările în baza de date
            click.secho(f"Client < {client_id} > was succesfully updated", fg="green")
            return
        except Client.DoesNotExist:
            click.secho(f"Client < {client_id} > not found")
        except Exception as e:
            # Gestionează alte erori posibile
            click.secho(
                f"Something went wrong wen we tried to update client < {client_id} >",
                fg="red",
            )
            return

    @staticmethod
    def delete_client(client_id):
        try:
            client = Client.objects.get(id=client_id)
            client.delete()
            click.secho(f"Client {client_id} was deleted", fg="green")
            return
        except ObjectDoesNotExist:
            click.secho(f"Client {client_id} doesn't exists", fg="red")
            return
