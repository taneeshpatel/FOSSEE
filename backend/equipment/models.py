"""
Models for the equipment app.
"""
from django.db import models
from django.conf import settings


class UploadedDataset(models.Model):
    """Stores uploaded CSV data for chemical equipment parameters."""
    # Owner of this dataset (used to isolate history per user)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_datasets',
        null=True,
        blank=True,
    )
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    raw_data = models.JSONField(default=list)  # Parsed CSV rows as list of dicts

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        owner = getattr(self.user, 'username', 'unknown-user')
        return f"{self.file_name} ({owner} @ {self.uploaded_at})"


class DataSummary(models.Model):
    """One-to-one summary statistics for an UploadedDataset."""
    dataset = models.OneToOneField(
        UploadedDataset,
        on_delete=models.CASCADE,
        related_name='summary'
    )
    total_count = models.FloatField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()
    type_distribution = models.JSONField(default=dict)  # e.g. {"Pump": 5, "Valve": 3}
    # Per-type: {"Pump": {"count": 5, "avg_temperature": 76.5, "avg_pressure": 12.1}, ...}
    type_stats = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Summary for {self.dataset.file_name}"
