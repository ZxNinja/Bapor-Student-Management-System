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
    enrollment_date = models.DateField(auto_now_add=True) # Automatically sets the date when student is added

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

class Paper(models.Model):
    """
    Represents an assignment, quiz, or exam.
    It defines the type of assessment and its total possible score.
    """
    PAPER_TYPES = (
        ('activity', 'Activity'),
        ('quiz', 'Quiz'),
        ('exam', 'Exam'),
    )

    name = models.CharField(max_length=200, help_text="Name of the paper (e.g., 'Midterm Exam', 'Homework 1')")
    paper_type = models.CharField(max_length=10, choices=PAPER_TYPES, help_text="Type of assessment (Activity, Quiz, Exam)")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='papers', help_text="The subject this paper belongs to")
    total_score = models.DecimalField(max_digits=5, decimal_places=2, help_text="Maximum possible score for this paper")
    date_assigned = models.DateField(auto_now_add=True, help_text="Date the paper was created/assigned")

    def __str__(self):
        """String representation of the Paper object."""
        return f"{self.name} ({self.subject.code} - {self.get_paper_type_display()})"

    class Meta:
        # Ensures that a paper name is unique within a subject for a given type
        unique_together = ('name', 'subject', 'paper_type')
        ordering = ['subject', 'date_assigned', 'name']


class Grade(models.Model):
    """
    Represents a grade for a specific student on a specific paper.
    Each grade is linked to a Paper, which defines its type (Activity, Quiz, Exam).
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades', help_text="The student who received this grade")
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name='grades', help_text="The paper for which this grade was given")
    score = models.DecimalField(max_digits=5, decimal_places=2, help_text="Score obtained by the student on this paper")
    date_recorded = models.DateField(auto_now_add=True, help_text="Date the grade was recorded")
    notes = models.TextField(blank=True, null=True, help_text="Additional notes about the grade")

    def __str__(self):
        """String representation of the Grade object."""
        return f"{self.student.first_name} {self.student.last_name} - {self.paper.name}: {self.score}/{self.paper.total_score}"

    class Meta:
        # Ensures a student has only one grade for a particular paper
        unique_together = ('student', 'paper')
        ordering = ['student', 'paper__subject', 'paper__name', 'date_recorded']

