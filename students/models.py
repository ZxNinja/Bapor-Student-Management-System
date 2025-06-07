# students/models.py
# Database models for the Student Management System.

from django.db import models

class Student(models.Model):
    """
    Represents a student.
    Fields for identification and basic demographic information.
    """
    student_id = models.CharField(
        max_length=20,
        unique=True,
        help_text="A unique identifier for the student (e.g., student ID number)."
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(
        unique=True,
        help_text="Unique email address for the student."
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text="Student's date of birth (optional)."
    )
    enrollment_date = models.DateField(
        auto_now_add=True,
        help_text="Date when the student was first enrolled or added to the system."
    )

    class Meta:
        # Default ordering for students in queries.
        ordering = ['last_name', 'first_name']
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        """Returns the full name and student ID for easy identification."""
        return f"{self.first_name} {self.last_name} ({self.student_id})"

class Subject(models.Model):
    """
    Represents an academic subject or course.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Full name of the subject (e.g., 'Mathematics', 'Computer Science Fundamentals')."
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        help_text="Short, unique code for the subject (e.g., 'MATH101', 'CS101')."
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed description of the subject content."
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        """Returns the subject name and code."""
        return f"{self.name} ({self.code})"

class Paper(models.Model):
    """
    Represents an assessment or assignment (e.g., activity, quiz, exam) within a subject.
    Defines the total possible score for this assessment.
    """
    # Choices for the type of paper/assessment.
    PAPER_TYPE_CHOICES = (
        ('activity', 'Activity'),
        ('quiz', 'Quiz'),
        ('exam', 'Exam'),
    )

    name = models.CharField(
        max_length=200,
        help_text="Name of the specific paper/assessment (e.g., 'Midterm Exam', 'Chapter 1 Quiz', 'Homework 1')."
    )
    paper_type = models.CharField(
        max_length=10,
        choices=PAPER_TYPE_CHOICES,
        help_text="Category of the paper (Activity, Quiz, or Exam)."
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='papers', # Allows accessing papers from a Subject instance (e.g., subject.papers.all())
        help_text="The subject to which this paper belongs."
    )
    total_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="The maximum achievable score for this paper."
    )
    date_assigned = models.DateField(
        auto_now_add=True,
        help_text="The date when this paper record was created."
    )

    class Meta:
        # Ensures that a paper with the same name, type, and subject is unique.
        unique_together = ('name', 'subject', 'paper_type')
        ordering = ['subject__name', 'paper_type', 'name'] # Order by subject, then type, then name
        verbose_name = "Paper"
        verbose_name_plural = "Papers"

    def __str__(self):
        """Returns a descriptive string for the paper."""
        return f"{self.name} ({self.get_paper_type_display()}) - {self.subject.code}"


class Grade(models.Model):
    """
    Represents a student's achieved score on a specific Paper.
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='grades', # Allows accessing grades from a Student instance (e.g., student.grades.all())
        help_text="The student who received this grade."
    )
    paper = models.ForeignKey(
        Paper,
        on_delete=models.CASCADE,
        related_name='grades', # Allows accessing grades from a Paper instance (e.g., paper.grades.all())
        help_text="The paper (activity, quiz, or exam) for which this grade was awarded."
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="The score obtained by the student on this paper."
    )
    date_recorded = models.DateField(
        auto_now_add=True,
        help_text="The date when this grade was officially recorded."
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Any additional remarks or comments about the grade."
    )

    class Meta:
        # Ensures that a student can only have one grade record for a specific paper.
        unique_together = ('student', 'paper')
        # Order grades by student, then subject of the paper, then paper name, then date.
        ordering = ['student__last_name', 'student__first_name', 'paper__subject__name', 'paper__name', 'date_recorded']
        verbose_name = "Grade"
        verbose_name_plural = "Grades"

    def __str__(self):
        """Returns a descriptive string for the grade."""
        return f"{self.student.first_name} {self.student.last_name} - {self.paper.name}: {self.score}/{self.paper.total_score}"

