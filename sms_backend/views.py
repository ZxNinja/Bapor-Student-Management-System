# sms_backend/views.py
# This file will contain simple views for the main project.

from django.http import JsonResponse

def api_root_status(request):
    """
    A simple view to indicate that the API is running.
    This will be accessible at the root URL (e.g., http://127.0.0.1:8000/).
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
