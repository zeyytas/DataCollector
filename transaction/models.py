import uuid

from django.db import models


class Transaction(models.Model):
    """
    Model representing a transaction.
    """

    STATUS_CHOICES = [
        (PURCHASE := 1, "purchase"),
        (REFUND := 2, "refund")
    ]

    product_id = models.UUIDField(default=uuid.uuid4)
    date_of_transaction = models.DateField()
    status = models.IntegerField(choices=STATUS_CHOICES)
    store_id = models.CharField(max_length=16)
