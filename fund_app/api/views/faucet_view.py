from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from ..serializers import FundWalletSerializer, FaucetStatsSerializer
from ...services.ethereum_service import EthereumService
from ...services.stats_service import StatsService


class FaucetViewSet(ViewSet):
    """
    ViewSet for handling faucet operations.

    This ViewSet provides endpoints for:
    - Funding wallets with test ETH
    - Retrieving faucet statistics
    - Testing transactions
    """
    serializer_class = FundWalletSerializer
    ethereum_service = EthereumService()
    stats_service = StatsService()
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def get_serializer(self, *args, **kwargs):
        """Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output."""
        serializer_class = self.serializer_class
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        """Extra context provided to the serializer class."""
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def _handle_get_request(self):
        """Handle GET requests for form views."""
        serializer = self.get_serializer()
        return Response(serializer.data)

    def _validate_wallet_address(self, request_data):
        """
        Validate wallet address from request data.
        Returns (wallet_address, None) if valid, (None, error_response) if invalid.
        """
        serializer = self.get_serializer(data=request_data)
        if not serializer.is_valid():
            return None, Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return serializer.validated_data["wallet_address"], None

    def _handle_transaction_result(self, result):
        """Handle the response from ethereum service."""
        if result["success"]:
            return Response(
                {
                    "message": result["message"],
                    "transaction_id": result["transaction_id"]
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": result["error"]},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @action(detail=False, methods=["get", "post"], url_path="fund-wallet")
    def fund_wallet(self, request):
        """
        Fund a wallet with test ETH.

        GET:
        Returns a form for entering wallet address.

        POST:
        Sends a specified amount of test ETH to the provided wallet address.
        No rate limiting - users can request as many times as they want.
        """
        if request.method == "GET":
            return self._handle_get_request()

        wallet_address, error_response = self._validate_wallet_address(request.data)
        if error_response:
            return error_response

        result = self.ethereum_service.fund_wallet(wallet_address)
        return self._handle_transaction_result(result)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        Get faucet statistics.

        Returns total, successful, and failed transaction counts.
        """
        stats = self.stats_service.get_faucet_stats()
        serializer = FaucetStatsSerializer(stats)
        return Response(serializer.data)

    @action(detail=False, methods=["get", "post"], url_path="test-transaction")
    def test_transaction(self, request):
        """
        Test a transaction without sending funds.

        GET:
        Returns a form for entering wallet address.

        POST:
        Simulates a transaction and logs it without actually sending any ETH.
        """
        if request.method == "GET":
            return self._handle_get_request()

        wallet_address, error_response = self._validate_wallet_address(request.data)
        if error_response:
            return error_response

        result = self.ethereum_service.fund_wallet(wallet_address, test_mode=True)
        return self._handle_transaction_result(result)
