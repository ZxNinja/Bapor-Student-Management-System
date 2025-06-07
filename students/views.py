# students/views.py
# This file defines the viewsets for our RESTful API.
# Viewsets provide actions like list, create, retrieve, update, and destroy
# for a model, abstracting common CRUD operations.

from rest_framework import viewsets
from .models import Student, Subject, Grade
from .serializers import StudentSerializer, SubjectSerializer, GradeSerializer
from rest_framework import permissions # For setting permissions
from rest_framework.filters import SearchFilter # For adding search capabilities

class StudentViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing student instances.
    Provides full CRUD operations for Student objects.
    Includes search functionality by first_name, last_name, and student_id.
    """
    queryset = Student.objects.all() # The set of objects that this view will operate on
    serializer_class = StudentSerializer # The serializer to use for input validation and output serialization
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Example permission: authenticated users can edit, others can only read

    # Add search filter to allow querying by student ID or name
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'student_id']


class SubjectViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing subject instances.
    Provides full CRUD operations for Subject objects.
    Includes search functionality by name and code.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Add search filter to allow querying by subject name or code
    filter_backends = [SearchFilter]
    search_fields = ['name', 'code']


class GradeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing grade instances.
    Provides full CRUD operations for Grade objects.
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # You can add custom filtering if needed, e.g., to filter grades by student or subject
    # This example demonstrates filtering by student_id from query parameters.
    def get_queryset(self):
        queryset = Grade.objects.all().select_related('student', 'subject') # Optimize with select_related
        student_id_param = self.request.query_params.get('student_id', None)
        subject_id_param = self.request.query_params.get('subject_id', None)

        if student_id_param is not None:
            queryset = queryset.filter(student__id=student_id_param) # Filter by student's primary key
        if subject_id_param is not None:
            queryset = queryset.filter(subject__id=subject_id_param) # Filter by subject's primary key

        return queryset
