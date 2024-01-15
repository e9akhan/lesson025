"""
    Module name :- urls
"""

from django.urls import path
from api import views

urlpatterns = [
    path("contacts/", views.contact, name="contact"),
    path("contacts/<int:pk>/", views.contact_with_pk),
]
