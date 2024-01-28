import click
import django
import os
import json
from datetime import datetime
from tabulate import tabulate
from employee.decorators import token_required, role_required
from employee.scripts import generate_token

# Setarea variabilelor de mediu pentru Django și inițializarea Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EpicEvents.settings")
django.setup()

# Importul modelelor și a altor componente necesare
from clients.views import Client
from events.views import Event
from employee.views import EmployeeService
from clients.views import ClientCRUD
from contracts.views import ContractCRUD
from events.views import EventCRUD


class EmployeeCLI:
    # LOGIN
    @staticmethod
    @click.command()
    @click.option("--email", prompt=True, hide_input=False, confirmation_prompt=False)
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=False)
    def login(email, password):
        try:
            if EmployeeService.authenticate(email, password):
                generate_token(email)
                click.secho("Login successful", fg="green")
            else:
                click.secho("Login failed: Invalid credentials", fg="red")
        except Exception as e:
            click.secho(f"An error occurred: {str(e)}", fg="red")

    # REGISTER
    @staticmethod
    @click.command()
    @click.argument("json_file", type=click.File("r"))
    def register(json_file):
        data = json.load(json_file)  # Folosește json.load pentru a citi din fișier

        for employee in data["employees"]:
            name = employee["name"]
            email = employee["email"]
            department = employee["department"]
            password = employee["password"]
            register_employee = EmployeeService.register(
                name, email, department, password
            )
            click.echo(register_employee)

    @staticmethod
    @click.command()
    @click.argument("email")
    @token_required
    def list_employee(email):
        employee = EmployeeService.get_employee(email)
        if employee:
            headers = ["Id", "Name", "Email", "Department"]
            click.secho(tabulate(employee, headers, tablefmt="grid"))
        else:
            click.secho(f"No employee found with email: {email}", fg="red")

    # LIST ALL EMPLOYEES
    @staticmethod
    @click.command()
    @token_required
    def list_employees():
        employees = EmployeeService.get_employees()
        print(employees)
        headers = ["Id", "Name", "Email", "Department"]
        click.echo(tabulate(employees, headers, tablefmt="grid"))

    @staticmethod
    def get_connected_employee():
        with open("secrets/employee_token.json", "r") as file:
            data = json.load(file)
            email = data.get("email")
            return EmployeeService.get_employee_object_by_email(email)


class ClientCLI:
    # ADD CLIENT
    @staticmethod
    @click.command()
    @click.argument("json_file", type=click.File("r"))
    @token_required
    def add_client(json_file):
        data = json.load(json_file)
        employee = EmployeeCLI.get_connected_employee()
        for client in data["clients"]:
            full_name = client["full_name"]
            email = client["email"]
            phone = client["phone"]
            company_name = client["company_name"]
            ClientCRUD.create_client(full_name, email, phone, company_name, employee)
        return

    # GET ONE CLIENT
    @staticmethod
    @click.command()
    @click.argument("client_id")
    @token_required
    def list_client(client_id):
        client = ClientCRUD.get_client(client_id)
        if client:
            headers = [
                "Id",
                "Full Name",
                "Email",
                "Phone",
                "Company",
                "Created",
                "Employee Id",
                "Last updated",
            ]

            click.echo(tabulate(client, headers, tablefmt="grid"))

    # GET ALL CLIENTS
    @staticmethod
    @click.command()
    @token_required
    @role_required("Sales")
    def list_clients():
        clients = ClientCRUD.get_all_clients()
        if clients:
            headers = [
                "Id",
                "Full Name",
                "Email",
                "Phone",
                "Company",
                "Created",
                "Employee Id",
                "Last updated",
            ]
            click.echo(tabulate(clients, headers, tablefmt="grid"))

    # UPDATE CLIENT
    @staticmethod
    @click.command()
    @click.argument("json_file", type=click.File("r"))
    @token_required
    def update_client(json_file):
        data = json.load(json_file)  # Folosește json.load pentru a citi din fișier
        for client in data["clients"]:
            id = client["id"]
            full_name = client["full_name"] if "full_name" in client else ""
            email = client["email"] if "email" in client else ""
            phone = client["phone"] if "phone" in client else ""
            company_name = client["company_name"] if "company_name" in client else ""
            ClientCRUD.update_client(
                client_id=id,
                full_name=full_name,
                email=email,
                phone=phone,
                company_name=company_name,
            )
        return

    # DELETE CLIENT
    @staticmethod
    @click.command()
    @click.argument("client_id")
    @token_required
    def delete_client(client_id):
        client = ClientCRUD.delete_client(client_id)
        return


class ContractCLI:
    # ADD CONTRACT
    @staticmethod
    @click.command()
    @click.argument("json_file", type=click.File("r"))
    @token_required
    def add_contract(json_file):
        data = json.load(json_file)
        employee = EmployeeCLI.get_connected_employee()
        for contract in data["contracts"]:
            client_id = contract["client_id"]
            total_amount = contract["total_amount"]
            amount_due = contract["amount_due"]
            status = contract["status"]
            ContractCRUD.create_contract(
                client_id, employee.pk, total_amount, amount_due, status
            )
        return

    # GET ONE CONTRACT
    @staticmethod
    @click.command()
    @click.argument("contract_id")
    @token_required
    def list_contract(contract_id):
        contract = ContractCRUD.get_contract(contract_id)
        if contract:
            headers = [
                "Id",
                "Total Amount",
                "Amount Due",
                "Creation Date",
                "Status",
                "Client Id",
                "Employee Id",
            ]

            click.echo(tabulate(contract, headers, tablefmt="grid"))

    # GET ALL CONTRACTS
    @staticmethod
    @click.command()
    @token_required
    def list_contracts():
        contracts = ContractCRUD.get_contracts()
        if contracts:
            headers = [
                "Id",
                "Total Amount",
                "Amount Due",
                "Creation Date",
                "Status",
                "Client",
                "Employee",
            ]
            click.echo(tabulate(contracts, headers, tablefmt="grid"))

    # UPDATE CONTRACT
    @staticmethod
    @click.command()
    @click.argument("json_file", type=click.File("r"))
    @token_required
    def update_contract(json_file):
        data = json.load(json_file)
        for contract in data["contracts"]:
            id = contract["id"] if "id" in contract else ""
            total_amount = (
                contract["total_amount"] if "total_amount" in contract else ""
            )
            amount_due = contract["amount_due"] if "amount_due" in contract else ""
            status = contract["status"] if "status" in contract else ""
            client = contract["client_id"] if "client_id" in contract else ""
            employee = contract["employee_id"] if "employee_id" in contract else ""

            if client != "":
                client = ClientCRUD.get_client_object(contract["client_id"])
            if employee != "":
                employee = EmployeeService.get_employee_object_by_id(
                    contract["employee_id"]
                )
            ContractCRUD.update_contract(
                contract_id=id,
                total_amount=total_amount,
                amount_due=amount_due,
                status=status,
                client=client,
                employee=employee,
            )

    # DELETE CONTRACT
    @staticmethod
    @click.command()
    @click.argument("contract_id")
    @token_required
    def delete_contract(contract_id):
        contract = ContractCRUD.delete_contract(contract_id)
        return


class EventCLI:
    # ADD EVENT
    @staticmethod
    @click.command()
    @click.argument("json_file", type=click.File("r"))
    @token_required
    def add_event(json_file):
        data = json.load(json_file)
        employee = EmployeeCLI.get_connected_employee()
        for event in data["events"]:
            contract_id = event["contract_id"]
            event_start_date = event["event_start_date"]
            event_end_date = event["event_end_date"]
            location = event["location"]
            attendees = event["attendees"]
            notes = event["notes"]
            EventCRUD.create_event(
                contract_id,
                event_start_date,
                event_end_date,
                employee.pk,
                location,
                attendees,
                notes,
            )
        return

    # GET ONE EVENT
    @staticmethod
    @click.command()
    @click.argument("event_id")
    @token_required
    def list_event(event_id):
        event = EventCRUD.get_event(event_id)
        if event:
            headers = [
                "Id",
                "Contract",
                "Event Start Date",
                "Event End Date",
                "Employee",
                "Location",
                "Attendees",
                "Notes",
            ]

            click.echo(tabulate(event, headers, tablefmt="grid"))

    # GET ALL EVENTS
    @staticmethod
    @click.command()
    @token_required
    def list_events():
        events = EventCRUD.get_events()
        if events:
            headers = [
                "Id",
                "Contract",
                "Event Start Date",
                "Event End Date",
                "Employee",
                "Location",
                "Attendees",
                "Notes",
            ]
            click.echo(tabulate(events, headers, tablefmt="grid"))

    # UPDATE EVENT
    @staticmethod
    @click.command()
    @click.argument("json_file", type=click.File("r"))
    @token_required
    def update_event(json_file):
        data = json.load(json_file)
        for event in data["events"]:
            id = event["id"] if "id" in event else ""
            contract_id = event["contract_id"] if "contract_id" in event else ""
            event_start_date = (
                event["event_start_date"] if "event_start_date" in event else ""
            )
            event_end_date = (
                event["event_end_date"] if "event_end_date" in event else ""
            )
            employee = event["employee"] if "employee" in event else ""
            location = event["location"] if "location" in event else ""
            attendees = event["attendees"] if "attendees" in event else ""
            notes = event["notes"] if "notes" in event else ""

            if employee != "":
                employee = EmployeeService.get_employee_object_by_id(event["employee"])
            EventCRUD.update_event(
                event_id=id,
                contract_id=contract_id,
                event_start_date=event_start_date,
                event_end_date=event_end_date,
                employee=employee,
                location=location,
                attendees=attendees,
                notes=notes,
            )

    # DELETE EVENT
    @staticmethod
    @click.command()
    @click.argument("event_id")
    @token_required
    def delete_event(event_id):
        event = EventCRUD.delete_event(event_id)
        return


@click.group()
def cli():
    pass


# EMPLOYEE
cli.add_command(EmployeeCLI.register, "register")
cli.add_command(EmployeeCLI.login, "login")
cli.add_command(EmployeeCLI.list_employees, "list-employees")
cli.add_command(EmployeeCLI.list_employee, "list-employee")

# CLIENT
cli.add_command(ClientCLI.add_client, "add-client")
cli.add_command(ClientCLI.update_client, "update-client")
cli.add_command(ClientCLI.list_client, "list-client")
cli.add_command(ClientCLI.list_clients, "list-clients")
cli.add_command(ClientCLI.delete_client, "delete-client")

# CONTRACT
cli.add_command(ContractCLI.add_contract, "add-contract")
cli.add_command(ContractCLI.update_contract, "update-contract")
cli.add_command(ContractCLI.list_contract, "list-contract")
cli.add_command(ContractCLI.list_contracts, "list-contracts")
cli.add_command(ContractCLI.delete_contract, "delete-contract")


# EVENTS
cli.add_command(EventCLI.add_event, "add-event")
cli.add_command(EventCLI.update_event, "update-event")
cli.add_command(EventCLI.list_event, "list-event")
cli.add_command(EventCLI.list_events, "list-events")
cli.add_command(EventCLI.delete_event, "delete-event")

if __name__ == "__main__":
    cli()
