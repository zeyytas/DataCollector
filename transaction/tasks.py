import json
import logging
import uuid
from random import randint

import requests
from celery import shared_task
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

logger = logging.getLogger(__name__)

TRANSACTION_API_URL = "http://web:8000"


def create_random_transaction_data() -> dict:
    """
    Generate random transaction data for simulating transaction creation.

    Returns:
        dict: Randomly generated transaction data.
    """
    random_data = {
        "product_id": str(uuid.uuid4()),
        "date_of_transaction": f"2025-{randint(1, 12):02d}-{randint(1, 28):02d}",
        "transaction_status": randint(1, 2),
        "store_id": randint(1, 3000),
    }
    return random_data


def generate_jwt_token() -> str:
    """
    Generate a JWT token for authentication.

    Returns:
        str: JWT token string.
    """
    user = User.objects.first()  # Which is created here transaction/migrations/0002_create_user.py
    token = AccessToken.for_user(user)
    return str(token)


def send_data_to_api(data):
    """
    Send transaction data to the API endpoint.

    Args:
        data (dict): Transaction data to be sent to the API.

    Returns:
        requests.Response: Response object from the API.
    """
    transaction_url = TRANSACTION_API_URL + reverse("transaction-list")
    access_token = generate_jwt_token()
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
    try:
        response = requests.post(transaction_url, headers=headers, json=data)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logger.error(f"Failed to send data to API: {str(e)}")
        raise


@shared_task
def create_transactions():
    """
    Task to create transactions by sending data to the API endpoint.

    Raises:
        Exception: If an error occurs during transaction creation.
    """
    try:
        logger.info("START: Creating transaction object")
        data = create_random_transaction_data()
        response = send_data_to_api(data)
        logger.info(f"FINISH: Transaction object created successfully. Response: {response.status_code}")

    except Exception as e:
        logger.error(f"An error occurred during transaction creation: {str(e)}")
