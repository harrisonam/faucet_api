from ..models import TransactionLog

class StatsService:
    """Service for handling faucet statistics."""

    @staticmethod
    def get_faucet_stats():
        """Get faucet statistics."""
        total_transactions = TransactionLog.objects.count()
        successful_transactions = TransactionLog.objects.filter(
            status="SUCCESS"
        ).count()
        failed_transactions = TransactionLog.objects.filter(
            status="FAILED"
        ).count()

        return {
            "total_transactions": total_transactions,
            "successful_transactions": successful_transactions,
            "failed_transactions": failed_transactions,
        }
