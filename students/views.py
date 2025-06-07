# students/views.py
# ViewSets for the RESTful API, providing CRUD operations for models.

from rest_framework import viewsets
from rest_framework.filters import SearchFilter
# Optional: import permissions if you want to apply authentication/authorization
# from rest_framework import permissions

from .models import Student, Subject, Paper, Grade
from .serializers import StudentSerializer, SubjectSerializer, PaperSerializer, GradeSerializer

class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows students to be viewed or edited.
    Supports search by first name, last name, and student ID.
    """
    queryset = Student.objects.all().order_by('last_name', 'first_name') # Ensure consistent ordering
    serializer_class = StudentSerializer
    # Example permission: Only authenticated users can modify, anyone can read.
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'student_id', 'email'] # Added email to search fields


class SubjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows subjects to be viewed or edited.
    Supports search by subject name and code.
    """
    queryset = Subject.objects.all().order_by('name') # Ensure consistent ordering
    serializer_class = SubjectSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [SearchFilter]
    search_fields = ['name', 'code']


class PaperViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows papers (activities, quizzes, exams) to be viewed or edited.
    Supports search by name, type, and associated subject.
    Allows filtering by subject_id and paper_type.
    """
    # Optimized queryset to fetch related subject data in one query.
    queryset = Paper.objects.all().select_related('subject').order_by('subject__name', 'paper_type', 'name')
    serializer_class = PaperSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [SearchFilter]
    search_fields = ['name', 'paper_type', 'subject__name', 'subject__code']

    def get_queryset(self):
        """
        Optionally restricts the returned papers to a given subject or paper type,
        by filtering against a `subject_id` or `paper_type` query parameter in the URL.
        """
        queryset = super().get_queryset()
        subject_id = self.request.query_params.get('subject_id', None)
        paper_type = self.request.query_params.get('paper_type', None)

        if subject_id is not None:
            queryset = queryset.filter(subject__id=subject_id)
        if paper_type is not None:
            queryset = queryset.filter(paper_type=paper_type)

        return queryset


class GradeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows grades to be viewed or edited.
    Allows filtering by student_id, paper_id, subject_id (of the paper), and grade_type (of the paper).
    """
    # Optimized queryset to fetch related student, paper, and paper's subject data.
    queryset = Grade.objects.all().select_related('student', 'paper', 'paper__subject').order_by(
        'student__last_name', 'student__first_name', 'paper__subject__name', 'paper__name', 'date_recorded'
    )
    serializer_class = GradeSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Optionally restricts the returned grades based on query parameters
        like student ID, paper ID, subject ID, or paper type.
        """
        queryset = super().get_queryset()
        student_id = self.request.query_params.get('student_id', None)
        paper_id = self.request.query_params.get('paper_id', None)
        subject_id = self.request.query_params.get('subject_id', None)
        grade_type = self.request.query_params.get('grade_type', None)

        if student_id is not None:
            queryset = queryset.filter(student__id=student_id)
        if paper_id is not None:
            queryset = queryset.filter(paper__id=paper_id)
        if subject_id is not None:
            # Filter by the subject associated with the paper
            queryset = queryset.filter(paper__subject__id=subject_id)
        if grade_type is not None:
            # Filter by the paper type associated with the paper
            queryset = queryset.filter(paper__paper_type=grade_type)

        return queryset

