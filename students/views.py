# students/views.py
# This file defines the viewsets for our RESTful API.
# Viewsets provide actions like list, create, retrieve, update, and destroy
# for a model, abstracting common CRUD operations.

from rest_framework import viewsets
from .models import Student, Subject, Paper, Grade
from .serializers import StudentSerializer, SubjectSerializer, PaperSerializer, GradeSerializer
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


class PaperViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing paper instances (activities, quizzes, exams).
    Provides full CRUD operations for Paper objects.
    Includes search functionality by name, paper_type, and subject.
    """
    queryset = Paper.objects.all().select_related('subject') # Optimize with select_related for subject
    serializer_class = PaperSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [SearchFilter]
    search_fields = ['name', 'paper_type', 'subject__name', 'subject__code']

    def get_queryset(self):
        # Allow filtering by subject_id or paper_type
        queryset = super().get_queryset()
        subject_id_param = self.request.query_params.get('subject_id', None)
        paper_type_param = self.request.query_params.get('paper_type', None)

        if subject_id_param is not None:
            queryset = queryset.filter(subject__id=subject_id_param)
        if paper_type_param is not None:
            queryset = queryset.filter(paper_type=paper_type_param)

        return queryset


class GradeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing grade instances.
    Provides full CRUD operations for Grade objects.
    """
    # Optimize with select_related for related student and paper objects
    queryset = Grade.objects.all().select_related('student', 'paper__subject')
    serializer_class = GradeSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Allow filtering by student_id or paper_id (which implies subject and type)
    def get_queryset(self):
        queryset = super().get_queryset()
        student_id_param = self.request.query_params.get('student_id', None)
        paper_id_param = self.request.query_params.get('paper_id', None)
        subject_id_param = self.request.query_params.get('subject_id', None) # Filter by subject of the paper
        grade_type_param = self.request.query_params.get('grade_type', None) # Filter by type of the paper

        if student_id_param is not None:
            queryset = queryset.filter(student__id=student_id_param)
        if paper_id_param is not None:
            queryset = queryset.filter(paper__id=paper_id_param)
        if subject_id_param is not None:
            queryset = queryset.filter(paper__subject__id=subject_id_param)
        if grade_type_param is not None:
            queryset = queryset.filter(paper__paper_type=grade_type_param)

        return queryset

