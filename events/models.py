from django.db import models
from contracts.models import Contract
from employee.models import Employee


class Event(models.Model):
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, related_name="events"
    )
    event_start_date = models.DateTimeField()
    event_end_date = models.DateTimeField()
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name="events"
    )
    location = models.CharField(max_length=200)
    attendees = models.IntegerField()
    notes = models.TextField()

    def __str__(self):
        return f"Event {self.id} - {self.contract.client.full_name}"
