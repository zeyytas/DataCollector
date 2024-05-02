from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.v1.serializers import TransactionSerializer
from transaction.filters import CustomTransactionFilter
from transaction.models import Transaction


class TransactionViewSet(ModelViewSet):
    """
    ViewSet for managing Transaction objects.
    """
    queryset = Transaction.objects.all().order_by("id")
    pagination_class = PageNumberPagination
    serializer_class = TransactionSerializer
    filterset_class = CustomTransactionFilter
    permission_classes = [IsAuthenticated]
