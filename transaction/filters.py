from django_filters import rest_framework as filters

from transaction.models import Transaction


class CustomTransactionFilter(filters.FilterSet):
    """
    Custom filter class for TransactionViewSet.
    """
    transaction_status = filters.CharFilter(field_name="status")
    date_of_transaction = filters.DateFromToRangeFilter()

    class Meta:
        model = Transaction
        fields = [
            "store_id",
            "transaction_status",
            "product_id",
            "date_of_transaction",
        ]
