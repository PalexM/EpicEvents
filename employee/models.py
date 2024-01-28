import bcrypt
from django.db import models


class Employee(models.Model):
    class DepartmentChoices(models.TextChoices):
        SALES = "Sales", "Sales"
        SUPPORT = "Support", "Support"
        MANAGEMENT = "Management", "Management"

    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=100, choices=DepartmentChoices.choices)
    hashed_password = models.CharField(max_length=60)

    def set_password(self, password):
        self.hashed_password = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()
        ).decode()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.hashed_password.encode())

    def __str__(self):
        return self.name
