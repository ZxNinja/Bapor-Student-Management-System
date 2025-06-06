# students/admin.py
# This file registers your models with the Django admin site,
# allowing you to easily manage data through the web interface.

from django.contrib import admin
from .models import Student, Subject, Grade

# Register your models here.
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Grade)

# You can also customize the admin interface for each model, for example:
# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('student_id', 'first_name', 'last_name', 'email', 'enrollment_date')
#     search_fields = ('first_name', 'last_name', 'student_id', 'email')
#     list_filter = ('enrollment_date',)
#     date_hierarchy = 'enrollment_date'
