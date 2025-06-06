# students/apps.py
# This file defines the configuration for your 'students' Django application.

from django.apps import AppConfig


class StudentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'students'
    verbose_name = 'Student Management' # A human-readable name for the app in admin
