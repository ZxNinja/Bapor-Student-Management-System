# sms_backend/urls.py
# This is the main URL configuration for your Django project.
import os

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static # This helper is key for static files

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),

    # API endpoints (students, subjects, grades)
    path('api/', include('students.urls')),

    # Serve the index.html at the root URL (e.g., http://127.0.0.1:8000/)
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]

# IMPORTANT: ONLY add this line in development (when DEBUG is True).
# This tells Django to serve static files from STATIC_URL (e.g., /static/)
# It must be at the *end* of your urlpatterns to ensure other specific
# patterns (like API) are matched first.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'Frontend'))
