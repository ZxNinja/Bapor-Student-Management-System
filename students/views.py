

# students/views.py
# This file defines the viewsets for our RESTful API.
# Viewsets provide actions like list, create, retrieve, update, and destroy
# for a model, abstracting common CRUD operations.d

from rest_framework import viewsets
from .models import Student, Subject, Grade
from .serializers import StudentSerializer, SubjectSerializer, GradeSerializer
from rest_framework import permissions # For setting permissions

class StudentViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing student instances.
    Provides full CRUD operations for Student objects.
    """
    queryset = Student.objects.all() # The set of objects that this view will operate on
    serializer_class = StudentSerializer # The serializer to use for input validation and output serialization
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Example permission: authenticated users can edit, others can only read

class SubjectViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing subject instances.
    Provides full CRUD operations for Subject objects.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class GradeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing grade instances.
    Provides full CRUD operations for Grade objects.
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # You can add custom filtering if needed, e.g., to filter grades by student or subject
    # def get_queryset(self):
    #     queryset = Grade.objects.all()
    #     student_id = self.request.query_params.get('student_id', None)
    #     subject_id = self.request.query_params.get('subject_id', None)
    #     if student_id is not None:
    #         queryset = queryset.filter(student__student_id=student_id)
    #     if subject_id is not None:
    #         queryset = queryset.filter(subject__code=subject_id)
    #     return queryset
