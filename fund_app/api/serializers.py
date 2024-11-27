from rest_framework import serializers


class FundWalletSerializer(serializers.Serializer):
    """
    Serializer for funding wallet and test transaction requests.
    """
    wallet_address = serializers.CharField(
        max_length=42,
        min_length=42,
        help_text="Enter your Ethereum wallet address (42 characters starting with 0x)",
        default="0x0000000000000000000000000000000000000000"
    )

    def validate_wallet_address(self, value):
        """
        Validate wallet address format.
        """
        if not value.startswith('0x'):
            raise serializers.ValidationError("Wallet address must start with '0x'")
        return value


class FaucetStatsSerializer(serializers.Serializer):
    """
    Serializer for faucet statistics.
    """
    total_transactions = serializers.IntegerField(
        min_value=0,
        help_text="Total number of transactions processed"
    )
    successful_transactions = serializers.IntegerField(
        min_value=0,
        help_text="Number of successful transactions"
    )
    failed_transactions = serializers.IntegerField(
        min_value=0,
        help_text="Number of failed transactions"
    )
