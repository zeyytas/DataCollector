from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import AccessToken
from uuid import uuid4

from transaction.models import Transaction
from transaction.tests.factories.transaction_factory import TransactionFactory
from transaction.tests.factories.user_factory import UserFactory


class EventAPITests(APITestCase):
    """Test cases for the Transaction API endpoints."""
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.transaction_1 = TransactionFactory(
            store_id=1,
            date_of_transaction="2022-01-01",
            status=Transaction.PURCHASE,
        )
        cls.transaction_2 = TransactionFactory(
            store_id=2,
            date_of_transaction="2023-01-01",
            status=Transaction.REFUND,
        )

        cls.response_transaction_1 = cls._create_response_dict(cls.transaction_1)
        cls.response_transaction_2 = cls._create_response_dict(cls.transaction_2)

        cls.path = reverse('transaction-list')

    def setUp(self) -> None:
        self.client.force_authenticate(self.user)

    @staticmethod
    def _create_response_dict(transaction):
        return {
            "id": transaction.id,
            "store_id": transaction.store_id,
            "transaction_status": transaction.status,
            "product_id": transaction.product_id,
            "date_of_transaction": transaction.date_of_transaction,
        }

    def _get_with_token(self, token):
        self.client.logout()
        return self.client.get(self.path, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})

    def _assert_response(self, response, expected_data):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["results"], expected_data)

    def test_get_transaction_list_with_valid_token(self):
        """Test getting the store list with a valid access token."""
        response = self._get_with_token(AccessToken.for_user(self.user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_transaction_list_with_invalid_token(self):
        """Test getting the store list with an invalid access token."""
        response = self._get_with_token(uuid4())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_transaction_list(self):
        """Test getting the store list."""
        response = self.client.get(self.path)
        self._assert_response(response, [self.response_transaction_1, self.response_transaction_2])

    def test_filter_transaction_list_by_store_id(self):
        """Test filtering the transaction list by store id."""
        response = self.client.get(self.path, {"store_id": self.transaction_2.store_id})
        self._assert_response(response, [self.response_transaction_2])

    def test_filter_transaction_list_by_date_of_transaction_date(self):
        """Test filtering the hotel list by date of transaction."""
        response = self.client.get(self.path, {"date_of_transaction_after": "2022-05-01"})
        self._assert_response(response, [self.response_transaction_2])

    def test_filter_transaction_list_by_product_id(self):
        """Test filtering the transaction list by product ID."""
        response = self.client.get(self.path, {"product_id": self.transaction_1.product_id})
        self._assert_response(response, [self.response_transaction_1])

    def test_filter_transaction_list_by_transaction_status(self):
        """Test filtering the hotel list by status."""
        response = self.client.get(self.path, {"transaction_status": Transaction.PURCHASE})
        self._assert_response(response, [self.response_transaction_1])

    def test_create_transaction(self):
        """Test creating a new transaction."""
        data = {
            "product_id": self.transaction_1.product_id,
            "date_of_transaction": self.transaction_1.date_of_transaction,
            "transaction_status": Transaction.REFUND,
            "store_id": self.transaction_1.store_id,
        }

        response = self.client.post(self.path, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Transaction.objects.filter(product_id=data["product_id"]).exists())
