from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from transaction.models import Transaction


class TransactionSerializer(ModelSerializer):
    """
    Serializer class for serializing Transaction objects for read operations and input data validation.
    """
    store_id = serializers.IntegerField()
    transaction_status = serializers.ChoiceField(choices=[1, 2], source="status")
    date_of_transaction = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Transaction
        fields = ["id", "store_id",  "transaction_status", "product_id", "date_of_transaction"]
