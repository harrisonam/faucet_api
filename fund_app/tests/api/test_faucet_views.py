"""
Tests for the Faucet API views.
"""
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from fund_app.models import TransactionLog
from fund_app.tests.test_utils import generate_eth_account, FaucetTestCase

class FaucetViewSetTests(APITestCase, FaucetTestCase):
    """Test suite for the FaucetViewSet API views."""

    def setUp(self):
        """Set up test data."""
        super().setUp()
        self.fund_wallet_url = reverse('faucet-fund-wallet')
        self.test_transaction_url = reverse('faucet-test-transaction')
        self.stats_url = reverse('faucet-stats')

    @patch('fund_app.services.ethereum_service.EthereumService.fund_wallet')
    def test_fund_wallet_success(self, mock_fund_wallet):
        """Test successful wallet funding."""
        # Mock successful transaction
        expected_tx_id = '0x' + '1' * 64
        mock_fund_wallet.return_value = {
            'success': True,
            'transaction_id': expected_tx_id
        }

        data = {'wallet_address': self.valid_address}
        response = self.client.post(self.fund_wallet_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['transaction_id'], expected_tx_id)

    def test_fund_wallet_invalid_address(self):
        """Test funding with invalid wallet address."""
        data = {'wallet_address': self.invalid_address}
        response = self.client.post(self.fund_wallet_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('error', response.data)

    @patch('fund_app.services.ethereum_service.EthereumService.fund_wallet')
    def test_test_transaction_success(self, mock_fund_wallet):
        """Test successful transaction simulation."""
        expected_tx_id = 'test_tx_' + '1' * 64
        mock_fund_wallet.return_value = {
            'success': True,
            'transaction_id': expected_tx_id
        }

        data = {'wallet_address': self.valid_address}
        response = self.client.post(self.test_transaction_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertTrue(response.data['transaction_id'].startswith('test_tx_'))

    def test_get_stats(self):
        """Test retrieving faucet statistics."""
        # Create some test transactions
        TransactionLog.objects.create(
            wallet_address=self.valid_address,
            transaction_id='0x' + '1' * 64,
            status='SUCCESS',
            amount=self.test_amount
        )
        TransactionLog.objects.create(
            wallet_address=self.valid_address,
            transaction_id='0x' + '2' * 64,
            status='FAILED',
            amount=self.test_amount
        )

        response = self.client.get(self.stats_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_transactions'], 2)
        self.assertEqual(response.data['successful_transactions'], 1)
        self.assertEqual(response.data['failed_transactions'], 1)
        self.assertEqual(float(response.data['total_eth_distributed']), float(self.test_amount))

    def test_get_fund_wallet_form(self):
        """Test getting the fund wallet form view."""
        response = self.client.get(self.fund_wallet_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('wallet_address', response.data['fields'])

    def test_rate_limiting(self):
        """Test rate limiting for funding requests."""
        # Assuming rate limit is 5 requests per minute
        for _ in range(5):
            response = self.client.post(
                self.fund_wallet_url,
                {'wallet_address': self.valid_address},
                format='json'
            )
            self.assertNotEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        # The 6th request should be rate limited
        response = self.client.post(
            self.fund_wallet_url,
            {'wallet_address': self.valid_address},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
