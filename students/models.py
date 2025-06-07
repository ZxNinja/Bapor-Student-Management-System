# students/models.py
# This file defines the database models for our Student Management System.
# Models represent tables in the database and define the fields (columns)
# for each record.

from django.db import models

class Student(models.Model):
    """
    Represents a student in the system.
    Stores basic student details.
    """
    student_id = models.CharField(max_length=20, unique=True, help_text="Unique identifier for the student")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    enrollment_date = models.DateField(null=True, blank=True) # MODIFIED LINE

    def __str__(self):
        """String representation of the Student object."""
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    class Meta:
        # Orders students by last name and then first name by default
        ordering = ['last_name', 'first_name']

class Subject(models.Model):
    """
    Represents a subject offered in the school.
    """
    name = models.CharField(max_length=100, unique=True, help_text="Name of the subject (e.g., Mathematics, Science)")
    code = models.CharField(max_length=10, unique=True, help_text="Short code for the subject (e.g., MATH101)")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """String representation of the Subject object."""
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['name']

class Grade(models.Model):
    """
    Represents a grade for a specific student in a specific subject.
    Grades can be for activities, quizzes, or exams.
    """
    GRADE_TYPES = (
        ('activity', 'Activity'),
        ('quiz', 'Quiz'),
        ('exam', 'Exam'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades', help_text="The student who received this grade")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades', help_text="The subject for which the grade was given")
    grade_type = models.CharField(max_length=10, choices=GRADE_TYPES, help_text="Type of assessment (Activity, Quiz, Exam)")
    score = models.DecimalField(max_digits=5, decimal_places=2, help_text="Score obtained (e.g., 85.50)")
    date_recorded = models.DateField(auto_now_add=True, help_text="Date the grade was recorded")
    notes = models.TextField(blank=True, null=True, help_text="Additional notes about the grade")

    def __str__(self):
        """String representation of the Grade object."""
        return f"{self.student.first_name} {self.student.last_name} - {self.subject.code} ({self.grade_type}): {self.score}"

    class Meta:
        # Ensures that a student can only have one grade of a specific type
        # for a particular subject on a given date (optional, can be adjusted)
        # Unique together ensures uniqueness of the combination of fields.
        # This particular `unique_together` might be too strict if a student
        # has multiple activities/quizzes in a single day for the same subject.
        # A more flexible approach might be to allow multiple grades of the same type
        # and rely on the frontend or a specific 'assessment_name' field for distinction.
        # For simplicity, we'll keep it as is, but it's a point to consider for refinement.
        unique_together = ('student', 'subject', 'grade_type', 'date_recorded')
        ordering = ['student', 'subject', 'date_recorded', 'grade_type']
