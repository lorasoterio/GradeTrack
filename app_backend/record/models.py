from django.db import models

# Create your models here.
class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    class_field = models.ForeignKey('ClassSchedule', on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    final_grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    remarks = models.CharField(max_length=20, null=True, blank=True)
    enrolled_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    pre_midterm_grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    midterm_grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pre_final_grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    final_period_grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def calculate_final_grade(self):
        period_grades = self.period_grades.all()

        if not period_grades.exists():
            return None

        total = sum([pg.computed_grade for pg in period_grades if pg.computed_grade is not None])
        count = period_grades.filter(computed_grade__isnull=False).count()

        if count > 0:
            self.final_grade = round(total / count, 2)

            if self.final_grade >= 75:
                self.remarks = "Passed"
            elif self.final_grade >= 70:
                self.remarks = "Conditional"
            else:
                self.remarks = "Failed"

            self.save()
            return self.final_grade

        return None

    def __str__(self):
        return f"{self.student.last_name} enrolled in {self.class_field.subject.code}"
