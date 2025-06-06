# sms_backend/urls.py
# This is the main URL configuration for your Django project.

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

# Import your custom views for project-level endpoints (if any)
# from . import views as project_views # Example for a root API status view

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),

    # API endpoints for the 'students' app
    # This includes all URLs defined in students/urls.py under the 'api/' path.
    path('api/', include('students.urls')),

    # Serve the index.html from your frontend for the root URL.
    # This is useful if you are serving the frontend directly from Django.
    # HOWEVER, since your frontend is on GitHub Pages, this path is optional
    # for production, but harmless if left in for local dev testing.
    # If your frontend is truly separate, you might remove this line
    # or redirect it to your GitHub Pages URL.
    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    # Optional: A simple API status endpoint at the project root (e.g., /status)
    # path('status/', project_views.api_root_status, name='api_status'),
]

# IMPORTANT: ONLY add this line in development (when DEBUG is True).
# This tells Django to serve static files from STATIC_URL (e.g., /static/)
# It is NOT for production. Production servers (like Nginx/Apache) handle static files.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    # Note: For multiple STATICFILES_DIRS, you might need a loop or specific handling.
    # For a single 'Frontend' dir as defined in settings, this is fine.
