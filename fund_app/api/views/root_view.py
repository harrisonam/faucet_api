from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from collections import OrderedDict


class APIRoot(APIView):
    """
    API root view providing hyperlinks to all main endpoints.
    """

    def get(self, request, format=None):
        return Response(
            OrderedDict(
                [
                    (
                        "fund-wallet",
                        reverse("faucet-fund-wallet", request=request, format=format),
                    ),
                    ("stats", reverse("faucet-stats", request=request, format=format)),
                    (
                        "test-transaction",
                        reverse(
                            "faucet-test-transaction", request=request, format=format
                        ),
                    ),
                ]
            )
        )
