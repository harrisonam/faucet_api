from web3 import Web3
from decouple import config
from ..models import TransactionLog


class EthereumService:
    """Service for handling Ethereum blockchain operations."""

    def __init__(self):
        self.infura_project_id = config("INFURA_PROJECT_ID")
        self.faucet_wallet_private_key = config("FAUCET_WALLET_PRIVATE_KEY")
        self.faucet_wallet_address = config("FAUCET_WALLET_ADDRESS")
        self.faucet_amount = Web3.to_wei(config("FAUCET_AMOUNT", cast=float), "ether")
        self.web3_provider = Web3(
            Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{self.infura_project_id}")
        )

    def prepare_transaction(self, to_address):
        """Prepare an Ethereum transaction."""
        return {
            "to": to_address,
            "value": self.faucet_amount,
            "gas": 21000,
            "gasPrice": self.web3_provider.eth.gas_price,
            "nonce": self.web3_provider.eth.get_transaction_count(self.faucet_wallet_address),
            "chainId": 11155111,  # Sepolia Testnet Chain ID
        }

    def send_transaction(self, transaction):
        """Sign and send an Ethereum transaction."""
        signed_txn = self.web3_provider.eth.account.sign_transaction(
            transaction, self.faucet_wallet_private_key
        )
        tx_hash = self.web3_provider.eth.send_raw_transaction(signed_txn.raw_transaction)
        return tx_hash.hex()

    def fund_wallet(self, wallet_address, test_mode=False):
        """
        Send test ETH to a wallet address.
        
        Args:
            wallet_address (str): The Ethereum wallet address to fund
            test_mode (bool): If True, simulates the transaction without sending funds
        """
        try:
            transaction = self.prepare_transaction(wallet_address)
            tx_id = self.send_transaction(transaction)
            
            if not test_mode:
                # Log the transaction
                TransactionLog.objects.create(
                    wallet_address=wallet_address,
                    transaction_id=tx_id if tx_id else None,
                    status="SUCCESS"
                )

            return {
                "success": True,
                "transaction_id": tx_id,
                "message": "Test transaction simulated successfully" if test_mode else "Transaction sent successfully"
            }

        except Exception as e:
            if not test_mode:
                # Log the failed transaction
                TransactionLog.objects.create(
                    wallet_address=wallet_address,
                    status="FAILED"
                )
            return {
                "success": False,
                "error": str(e)
            }
