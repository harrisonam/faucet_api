"""
Tests for the StatsService.
"""
from decimal import Decimal
from django.test import TestCase
from fund_app.models import TransactionLog
from fund_app.services.stats_service import StatsService
from fund_app.tests.test_utils import generate_eth_account

class StatsServiceTests(TestCase):
    """Test suite for the StatsService."""

    def setUp(self):
        """Set up test data."""
        self.service = StatsService()
        self.test_account = generate_eth_account()
        
        # Create some test transactions
        self.successful_tx = TransactionLog.objects.create(
            wallet_address=self.test_account['address'],
            transaction_id='0x' + '1' * 64,
            status='SUCCESS',
            amount=Decimal('0.0001')
        )
        
        self.failed_tx = TransactionLog.objects.create(
            wallet_address=self.test_account['address'],
            transaction_id='0x' + '2' * 64,
            status='FAILED',
            amount=Decimal('0.0001')
        )
        
        self.pending_tx = TransactionLog.objects.create(
            wallet_address=self.test_account['address'],
            transaction_id='0x' + '3' * 64,
            status='PENDING',
            amount=Decimal('0.0001')
        )

    def test_get_faucet_stats(self):
        """Test retrieving faucet statistics."""
        stats = self.service.get_faucet_stats()
        
        self.assertEqual(stats['total_transactions'], 3)
        self.assertEqual(stats['successful_transactions'], 1)
        self.assertEqual(stats['failed_transactions'], 1)
        self.assertEqual(stats['pending_transactions'], 1)
        self.assertEqual(stats['total_eth_distributed'], '0.0001')

    def test_log_transaction(self):
        """Test logging a new transaction."""
        new_tx_id = '0x' + '4' * 64
        
        self.service.log_transaction(
            wallet_address=self.test_account['address'],
            transaction_id=new_tx_id,
            status='SUCCESS',
            amount=Decimal('0.0002')
        )
        
        # Verify the transaction was logged
        tx_log = TransactionLog.objects.get(transaction_id=new_tx_id)
        self.assertEqual(tx_log.wallet_address, self.test_account['address'])
        self.assertEqual(tx_log.status, 'SUCCESS')
        self.assertEqual(tx_log.amount, Decimal('0.0002'))

    def test_get_wallet_transactions(self):
        """Test retrieving transactions for a specific wallet."""
        transactions = self.service.get_wallet_transactions(self.test_account['address'])
        
        self.assertEqual(len(transactions), 3)
        self.assertTrue(all(tx.wallet_address == self.test_account['address'] 
                          for tx in transactions))

    def test_get_recent_transactions(self):
        """Test retrieving recent transactions."""
        transactions = self.service.get_recent_transactions(limit=2)
        
        self.assertEqual(len(transactions), 2)
        # Should be ordered by created_at descending
        self.assertTrue(transactions[0].created_at >= transactions[1].created_at)

    def test_get_transaction_by_id(self):
        """Test retrieving a specific transaction by ID."""
        transaction = self.service.get_transaction_by_id(self.successful_tx.transaction_id)
        
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.transaction_id, self.successful_tx.transaction_id)
        self.assertEqual(transaction.status, 'SUCCESS')
