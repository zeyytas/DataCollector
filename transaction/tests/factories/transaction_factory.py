from datetime import datetime

import factory
from factory import Faker
from factory.fuzzy import FuzzyNaiveDateTime, FuzzyInteger

from transaction.models import Transaction


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    product_id = Faker('uuid4')
    date_of_transaction = FuzzyNaiveDateTime(datetime(2024, 1, 1))
    status = Transaction.PURCHASE
    store_id = FuzzyInteger(42)
