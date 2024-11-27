"""
Tests for the EthereumService.
"""
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.conf import settings
from web3 import Web3
from fund_app.services.ethereum_service import EthereumService
from fund_app.tests.test_utils import generate_eth_account

class EthereumServiceTests(TestCase):
    """Test suite for the EthereumService."""

    def setUp(self):
        """Set up test data."""
        self.service = EthereumService()
        self.test_account = generate_eth_account()
        self.to_address = self.test_account['address']
        self.amount = 0.0001

    @patch('web3.Web3.eth')
    def test_prepare_transaction(self, mock_eth):
        """Test transaction preparation."""
        # Mock ethereum responses
        mock_eth.get_transaction_count.return_value = 1
        mock_eth.gas_price = 20000000000
        mock_eth.estimate_gas.return_value = 21000

        transaction = self.service.prepare_transaction(self.to_address)

        self.assertEqual(transaction['to'], self.to_address)
        self.assertEqual(transaction['value'], Web3.to_wei(self.amount, 'ether'))
        self.assertEqual(transaction['nonce'], 1)
        self.assertGreater(transaction['gas'], 0)
        self.assertGreater(transaction['gasPrice'], 0)

    @patch('web3.Web3.eth')
    def test_send_transaction(self, mock_eth):
        """Test sending a transaction."""
        # Mock transaction hash
        expected_hash = '0x' + '1' * 64
        mock_eth.send_raw_transaction.return_value = expected_hash

        transaction = {
            'to': self.to_address,
            'value': Web3.to_wei(self.amount, 'ether'),
            'gas': 21000,
            'gasPrice': 20000000000,
            'nonce': 1,
        }

        tx_hash = self.service.send_transaction(transaction)
        self.assertEqual(tx_hash, expected_hash)

    @patch('fund_app.services.ethereum_service.EthereumService.prepare_transaction')
    @patch('fund_app.services.ethereum_service.EthereumService.send_transaction')
    def test_fund_wallet(self, mock_send, mock_prepare):
        """Test the complete fund_wallet flow."""
        # Mock the internal methods
        prepared_tx = {'to': self.to_address, 'value': Web3.to_wei(self.amount, 'ether')}
        expected_hash = '0x' + '1' * 64
        
        mock_prepare.return_value = prepared_tx
        mock_send.return_value = expected_hash

        result = self.service.fund_wallet(self.to_address)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['transaction_id'], expected_hash)
        
        mock_prepare.assert_called_once_with(self.to_address)
        mock_send.assert_called_once_with(prepared_tx)

    def test_fund_wallet_invalid_address(self):
        """Test funding with an invalid address."""
        result = self.service.fund_wallet('invalid_address')
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
        self.assertIn('Invalid Ethereum address', result['error'])

    @patch('fund_app.services.ethereum_service.EthereumService.prepare_transaction')
    def test_fund_wallet_test_mode(self, mock_prepare):
        """Test fund_wallet in test mode."""
        result = self.service.fund_wallet(self.to_address, test_mode=True)
        
        self.assertTrue(result['success'])
        self.assertTrue(result['transaction_id'].startswith('test_tx_'))
        mock_prepare.assert_not_called()
