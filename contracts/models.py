from django.db import models
from clients.models import Client
from employee.models import Employee


class Contract(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="contracts"
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name="contracts"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)  # False = Not Signed, True = Signed

    def __str__(self):
        return f"Contract {self.id} - {self.client.full_name}"
