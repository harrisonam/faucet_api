"""
Test utilities and fixtures for the Ethereum Faucet API tests.
"""
from django.test import TestCase
from eth_account import Account
import eth_account
import secrets

def generate_eth_account():
    """Generate a random Ethereum account for testing."""
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    account = Account.from_key(private_key)
    return {
        'address': account.address,
        'private_key': private_key
    }

class FaucetTestCase(TestCase):
    """Base test case with common utilities for faucet tests."""
    
    def setUp(self):
        """Set up test data."""
        self.test_account = generate_eth_account()
        self.valid_address = self.test_account['address']
        self.invalid_address = "0xinvalid"
        self.test_amount = 0.0001
        
    def assertEthereumAddress(self, address):
        """Assert that a string is a valid Ethereum address."""
        self.assertTrue(eth_account.is_address(address))
        self.assertTrue(address.startswith('0x'))
        self.assertEqual(len(address), 42)  # '0x' + 40 hex chars
