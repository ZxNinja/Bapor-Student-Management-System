

# students/serializers.py
# This file defines serializers, which convert complex data types (like Django models)
# into native Python datatypes that can be easily rendered into JSON, XML, or other
# content types. They also provide deserialization to allow incoming data to be
# validated and saved into model instances.

from rest_framework import serializers
from .models import Student, Subject, Grade

class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Student model.
    Converts Student model instances to JSON and vice-versa.
    """
    # Define a custom field to get the full name for display purposes
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = '__all__' # Include all fields from the Student model
        # You can specify fields explicitly like:
        # fields = ['id', 'student_id', 'first_name', 'last_name', 'email', 'date_of_birth', 'enrollment_date', 'full_name']
        read_only_fields = ['enrollment_date'] # enrollment_date is set automatically

    def get_full_name(self, obj):
        """
        Method to get the full name of the student.
        Used by the `full_name` SerializerMethodField.
        """
        return f"{obj.first_name} {obj.last_name}"

class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subject model.
    """
    class Meta:
        model = Subject
        fields = '__all__' # Include all fields from the Subject model

class GradeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Grade model.
    Allows for nested representation of student and subject details.
    """
    # Use nested serializers to display related student and subject information.
    # This makes the API response more informative without extra lookups on the client.
    student = StudentSerializer(read_only=True) # Display full student object, read-only
    subject = SubjectSerializer(read_only=True) # Display full subject object, read-only

    # To allow creating/updating grades by sending student/subject IDs instead of full objects
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), source='student', write_only=True,
        help_text="ID of the student to whom this grade belongs"
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), source='subject', write_only=True,
        help_text="ID of the subject for which this grade was given"
    )

    class Meta:
        model = Grade
        fields = '__all__' # Include all fields from the Grade model
        # Explicitly list fields for clarity and control, especially with write_only fields
        # fields = ['id', 'student', 'subject', 'grade_type', 'score', 'date_recorded', 'notes', 'student_id', 'subject_id']
        read_only_fields = ['date_recorded'] # date_recorded is set automatically
