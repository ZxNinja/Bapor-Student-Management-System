# sms_backend/views.py
# This file can contain simple views for the main Django project,
# not necessarily related to a specific app.

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root_status(request):
    """
    A simple API endpoint to indicate that the API is running.
    This can be used for health checks or basic API discovery.
    """
    return JsonResponse({
        'status': 'ok',
        'message': 'Student Management System API is running!',
        'api_version': '1.0',
        'endpoints': {
            'students': '/api/students/',
            'subjects': '/api/subjects/',
            'grades': '/api/grades/',
            'admin': '/admin/'
        }
    })
