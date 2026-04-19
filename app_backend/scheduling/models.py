from django.db import models

# Create your models here.
class ClassSchedule(models.Model):
    class_id = models.AutoField(primary_key=True)
    term = models.ForeignKey('core.AcademicTerm', on_delete=models.CASCADE)
    subject = models.ForeignKey('core.Subject', on_delete=models.CASCADE)
    section = models.ForeignKey('students.Section', on_delete=models.CASCADE)
    teacher = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    room = models.CharField(max_length=50)
    days = models.CharField(max_length=100, blank=True, null=True, default='TBA')
    days_of_week = models.CharField(max_length=50, null=True, blank=True, help_text="e.g., M-W-F or T-Th")
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    schedule_text = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject.code} - {self.section.name} ({self.teacher.last_name})"


class TeacherSchedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    subject = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    time = models.CharField(max_length=100)
    room = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
