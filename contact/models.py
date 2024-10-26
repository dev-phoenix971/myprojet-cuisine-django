from django.contrib import admin
from django.db import models


class Contact(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    message = models.CharField(max_length=1000)