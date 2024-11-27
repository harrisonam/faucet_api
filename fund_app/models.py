from django.db import models


class TransactionLog(models.Model):
    wallet_address = models.CharField(max_length=42)
    transaction_id = models.CharField(max_length=66, null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('SUCCESS', 'Success'), ('FAILED', 'Failed')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet_address} - {self.status}"