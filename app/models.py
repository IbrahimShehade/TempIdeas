from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Qada(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Municipal(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    qada = models.ForeignKey(Qada, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name  


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True)
    qada = models.ForeignKey(Qada, on_delete=models.CASCADE, null=True, blank=True)
    municipal = models.ForeignKey(Municipal, on_delete=models.CASCADE, null=True, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    mobile_phone = PhoneNumberField()

   

    def calculate_age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year

            # Check if the user has already celebrated their birthday this year
            if today < date(today.year, self.date_of_birth.month, self.date_of_birth.day):
                age -= 1

            self.age = age
            self.save()


