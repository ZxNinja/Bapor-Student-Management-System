

# students/urls.py
# This file defines the URL routing for the 'students' app's API endpoints.
# Django REST Framework's routers automatically generate URL patterns
# for common API operations (list, create, retrieve, update, delete).

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, SubjectViewSet, GradeViewSet

# Create a router instance
router = DefaultRouter()

# Register our viewsets with the router.
# The `basename` argument is used to generate URL names, e.g., 'students-list', 'students-detail'.
# It's especially useful when a queryset is not provided in the ViewSet.
router.register(r'students', StudentViewSet, basename='student')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'grades', GradeViewSet, basename='grade')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
