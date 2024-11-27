"""
Tests for the TransactionLog model.
"""
from decimal import Decimal
from django.test import TestCase
from fund_app.models import TransactionLog
from fund_app.tests.test_utils import generate_eth_account

class TransactionLogModelTests(TestCase):
    """Test suite for the TransactionLog model."""

    def setUp(self):
        """Set up test data."""
        self.test_account = generate_eth_account()
        self.test_data = {
            'wallet_address': self.test_account['address'],
            'transaction_id': '0x' + '1' * 64,
            'status': 'SUCCESS',
            'amount': Decimal('0.0001')
        }

    def test_create_transaction_log(self):
        """Test creating a transaction log entry."""
        log = TransactionLog.objects.create(**self.test_data)
        self.assertEqual(log.wallet_address, self.test_data['wallet_address'])
        self.assertEqual(log.transaction_id, self.test_data['transaction_id'])
        self.assertEqual(log.status, self.test_data['status'])
        self.assertEqual(log.amount, self.test_data['amount'])

    def test_transaction_log_str(self):
        """Test the string representation of a transaction log."""
        log = TransactionLog.objects.create(**self.test_data)
        expected_str = f"{self.test_data['status']} - {self.test_data['wallet_address']}"
        self.assertEqual(str(log), expected_str)

    def test_transaction_log_status_choices(self):
        """Test that transaction log status must be one of the defined choices."""
        invalid_data = self.test_data.copy()
        invalid_data['status'] = 'INVALID_STATUS'
        
        with self.assertRaises(Exception):
            TransactionLog.objects.create(**invalid_data)

    def test_transaction_log_amount_validation(self):
        """Test that transaction amount must be positive."""
        invalid_data = self.test_data.copy()
        invalid_data['amount'] = Decimal('-0.0001')
        
        with self.assertRaises(Exception):
            TransactionLog.objects.create(**invalid_data)

    def test_transaction_log_defaults(self):
        """Test default values for transaction log fields."""
        minimal_data = {
            'wallet_address': self.test_data['wallet_address'],
            'transaction_id': self.test_data['transaction_id']
        }
        log = TransactionLog.objects.create(**minimal_data)
        
        self.assertIsNotNone(log.created_at)
        self.assertEqual(log.status, 'PENDING')  # Assuming PENDING is the default status
