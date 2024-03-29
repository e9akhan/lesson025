"""
    Module name :- models
    Classes :- Contact
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Contact(models.Model):
    """
    Data model for Contact.
    """

    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    phone_no = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="contacts", blank=True)
    starred = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def email_list(self):
        return self.email.split(",")

    @property
    def phone_no_list(self):
        return self.phone_no.split(",")

    @property
    def address_list(self):
        return self.address.split(",")

    def __str__(self):
        return f"{self.name}"
