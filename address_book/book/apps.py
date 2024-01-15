"""
    Module name :- apps
"""

from django.apps import AppConfig


class BookConfig(AppConfig):
    """
    Class for App configuration.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "book"
