from django.db import models
from django.contrib.auth.models import User

class Donation(models.Model):
    class Meta:
        permissions = (
          ('donation_mail', 'Recieves emails about new donations'),
        )

    STATUS_PENDING = 0
    STATUS_PAID = 1
    STATUS = (
      (STATUS_PENDING, 'Pending'),
      (STATUS_PAID, 'Paid'),
    )
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)
    quantity = models.FloatField()
    transactionId = models.TextField(blank=True, null=True)
    status = models.IntegerField(default=STATUS_PENDING, choices = STATUS)
    user = models.ForeignKey(User)

