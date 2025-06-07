# students/serializers.py
# Serializers for converting Django models to JSON and vice-versa.

from rest_framework import serializers
from .models import Student, Subject, Paper, Grade

class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Student model.
    Includes a 'full_name' computed field.
    """
    full_name = serializers.SerializerMethodField(
        help_text="Concatenated first and last name of the student."
    )

    class Meta:
        model = Student
        fields = '__all__' # Include all model fields
        read_only_fields = ['enrollment_date'] # Field set automatically on creation

    def get_full_name(self, obj):
        """
        Method to calculate the full name of the student.
        """
        return f"{obj.first_name} {obj.last_name}"

class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subject model.
    """
    class Meta:
        model = Subject
        fields = '__all__' # Include all model fields

class PaperSerializer(serializers.ModelSerializer):
    """
    Serializer for the Paper model.
    Handles nested subject representation for reading, and subject ID for writing.
    """
    subject = SubjectSerializer(
        read_only=True,
        help_text="Detailed subject information associated with this paper (read-only)."
    )
    # Use PrimaryKeyRelatedField for writing, allowing subject_id to be passed.
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source='subject', # Map to the 'subject' foreign key
        write_only=True, # Only used for input, not included in output
        help_text="The ID of the subject this paper belongs to (write-only)."
    )

    class Meta:
        model = Paper
        fields = '__all__' # Include all model fields, including subject_id for writes
        read_only_fields = ['date_assigned'] # Field set automatically on creation

class GradeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Grade model.
    Handles nested student and paper representation for reading, and IDs for writing.
    """
    student = StudentSerializer(
        read_only=True,
        help_text="Detailed student information (read-only)."
    )
    paper = PaperSerializer(
        read_only=True,
        help_text="Detailed paper information (read-only)."
    )
    # Use PrimaryKeyRelatedField for writing, allowing student_id and paper_id to be passed.
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        source='student', # Map to the 'student' foreign key
        write_only=True,
        help_text="The ID of the student receiving this grade (write-only)."
    )
    paper_id = serializers.PrimaryKeyRelatedField(
        queryset=Paper.objects.all(),
        source='paper', # Map to the 'paper' foreign key
        write_only=True,
        help_text="The ID of the paper for which this grade is given (write-only)."
    )

    class Meta:
        model = Grade
        fields = '__all__' # Include all model fields, including student_id and paper_id for writes
        read_only_fields = ['date_recorded'] # Field set automatically on creation

