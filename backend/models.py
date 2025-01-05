"""
Models for the backend application.
"""
from django.db import models

class Podcast(models.Model):
    """
    Model representing a podcast generated from a PDF.
    """
    STATUS_CHOICES = [
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("error", "Error"),
    ]

    file_name = models.CharField(max_length=255)  # Name of the uploaded PDF
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="processing")
    podcast_path = models.CharField(max_length=500, blank=True, null=True)  # Path to podcast
    created_at = models.DateTimeField(auto_now_add=True)  # Track when it was created
