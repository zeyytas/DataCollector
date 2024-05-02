from rest_framework import routers

from api.v1.views import TransactionViewSet

router = routers.DefaultRouter()

router.register(r'transactions', TransactionViewSet)
