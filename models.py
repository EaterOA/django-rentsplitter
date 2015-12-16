from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class User(models.Model):
    name    = models.CharField(max_length=100, unique=True)

class Rent(models.Model):
    amount  = models.DecimalField(max_digits=20, decimal_places=2)

class Entry(models.Model):
    amount  = models.DecimalField(max_digits=20, decimal_places=2)
    payer   = models.ForeignKey(User, on_delete=models.CASCADE)
    note    = models.CharField(max_length=4000)
    date    = models.DateTimeField(default=timezone.now)

class DebtEntry(Entry):
    payee   = models.ForeignKey(User, on_delete=models.CASCADE)

class UtilityEntry(Entry):
    pass
