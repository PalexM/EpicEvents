from django.db import models
from django.utils import timezone
from employee.models import Employee


class Client(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name="clients"
    )

    def __str__(self):
        return self.full_name
