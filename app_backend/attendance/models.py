from django.db import models

# Create your models here.
class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE)
    date_logged = models.DateField()
    status = models.CharField(max_length=20)
    reason = models.TextField(null=True, blank=True)

