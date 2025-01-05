"""
Admin configuration for the Podcast model.
"""
from django.contrib import admin
from .models import Podcast  # Import your Podcast model

@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    """
    Admin view for the Podcast model.
    """
    list_display = (
        'file_name', 
        'status', 
        'podcast_path', 
        'created_at')  # Fields to display in the admin list view
    list_filter = ('status',)  # Filters by status
    search_fields = ('file_name',)  # Add search functionality
