from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .models import Event
from employee.scripts import get_connected_employee_email
from employee.models import Employee
from django.core.exceptions import FieldError

import click


class EventCRUD:
    """CRUD OPERATIONS ARE HANDLED HERE"""

    @staticmethod
    def create_event(
        contract_id,
        event_start_date,
        event_end_date,
        employee_id,
        location,
        attendees,
        notes,
    ):
        if employee_id:
            try:
                if is_designed_salesman_part_of_support_team(employee_id):
                    Event.objects.create(
                        contract_id=contract_id,
                        event_start_date=event_start_date,
                        event_end_date=event_end_date,
                        employee_id=employee_id,
                        location=location,
                        attendees=attendees,
                        notes=notes,
                    )

                    click.secho(f"Event successfully created", fg="green")
                    return
                else:
                    click.secho(
                        f"The designated employee is not part of Suport team", fg="red"
                    )
                    return
            except IntegrityError as e:
                click.secho(f"Integrity error: {e}", fg="red")
                return
            except Exception as e:
                click.secho(f"Unexpected error: {e}", fg="red")
                return
        else:
            try:
                Event.objects.create(
                    contract_id=contract_id,
                    event_start_date=event_start_date,
                    event_end_date=event_end_date,
                    location=location,
                    attendees=attendees,
                    notes=notes,
                )

                click.secho(f"Event successfully created", fg="green")
                return
            except IntegrityError as e:
                click.secho(f"Integrity error: {e}", fg="red")
                return
            except Exception as e:
                click.secho(f"Unexpected error: {e}", fg="red")
                return

    @staticmethod
    def get_event(event_id):
        try:
            event = Event.objects.get(id=event_id)
            return [
                [
                    event.pk,
                    event.contract,
                    event.event_start_date,
                    event.event_end_date,
                    event.employee,
                    event.location,
                    event.attendees,
                    event.notes,
                ]
            ]
        except ObjectDoesNotExist:
            click.secho(f"Event {event_id} doesn't exist", fg="red")
            return False

    @staticmethod
    def get_events():
        try:
            events = Event.objects.all()

            table = []
            for event in events:
                table.append(
                    [
                        event.pk,
                        event.contract,
                        event.event_start_date,
                        event.event_end_date,
                        event.employee,
                        event.location,
                        event.attendees,
                        event.notes,
                    ]
                )
            return table

        except Exception as e:
            click.secho(f"Something went wrong: {e}", fg="red")
            return

    @staticmethod
    def filter_events(filter_criteria):
        try:
            events = Event.objects.filter(**filter_criteria)
            table = []
            for event in events:
                table.append(
                    [
                        event.pk,
                        event.contract,
                        event.event_start_date,
                        event.event_end_date,
                        event.employee,
                        event.location,
                        event.attendees,
                        event.notes,
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
    def update_event(event_id, **kwargs):
        try:
            event = Event.objects.get(id=event_id)
            for key, value in kwargs.items():
                if value not in [None, ""]:
                    setattr(event, key, value)
            event.save()
            click.secho(f"Event {event_id} was successfully updated", fg="green")
            return
        except ObjectDoesNotExist:
            click.secho(f"Event {event_id} doesn't exist", fg="red")
            return

    @staticmethod
    def delete_event(event_id):
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            click.secho(f"Event {event_id} was deleted", fg="green")
            return
        except ObjectDoesNotExist:
            click.secho(f"Event {event_id} doesn't exist", fg="red")
            return


def is_designed_salesman_part_of_support_team(employee_id):
    employee = Employee.objects.get(id=employee_id)
    return employee.department == "Support"
