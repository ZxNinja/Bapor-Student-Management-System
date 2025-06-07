# sms_backend/urls.py
# This is the main URL configuration for your Django project.

from django.contrib import admin
from django.urls import path, include
# No longer need TemplateView or static file serving for production
# from django.views.generic import TemplateView
# from django.conf import settings
# from django.conf.urls.static import static

# Import your custom views for project-level endpoints
from . import views as project_views # Import the project-level views

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),

    # API endpoints for the 'students' app
    # This includes all URLs defined in students/urls.py under the 'api/' path.
    path('api/', include('students.urls')),

    # A simple API status endpoint at the project root (e.g., /)
    # This will now serve the api_root_status view when the root URL is accessed.
    path('', project_views.api_root_status, name='api_status'), # Added this line!
]

# IMPORTANT: Remove this block for production deployment.
# This tells Django to serve static files from STATIC_URL (e.g., /static/)
# It is NOT for production. Production servers (like Render/WhiteNoise) handle static files.
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
