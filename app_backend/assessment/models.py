from django.db import models

# Create your models here.
class Assessment(models.Model):
    assessment_id = models.AutoField(primary_key=True)
    component = models.ForeignKey('GradingComponent', on_delete=models.CASCADE)
    period = models.ForeignKey('core.Period', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)

    ASSESSMENT_TYPES = [
        ('Quiz', 'Quiz'),
        ('Activity', 'Activity'),
        ('Exam', 'Exam'),
        ('Project', 'Project')
    ]
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPES, default='Activity')

    total_points = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    date_given = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.component.name})"


class StudentScore(models.Model):
    score_id = models.AutoField(primary_key=True)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)


# attendance
class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE)
    date_logged = models.DateField()
    status = models.CharField(max_length=20)
    reason = models.TextField(null=True, blank=True)


# grading
class GradingComponent(models.Model):
    component_id = models.AutoField(primary_key=True)
    class_field = models.ForeignKey('ClassSchedule', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    weight_percentage = models.DecimalField(max_digits=5, decimal_places=2)


class PeriodGrade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE, related_name='period_grades')
    period = models.ForeignKey('core.Period', on_delete=models.CASCADE)

    computed_grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('enrollment', 'period')

    def calculate_grade(self):
        total_period_grade = 0
        class_schedule = self.enrollment.class_field

        components = GradingComponent.objects.filter(class_field=class_schedule)

        for component in components:
            assessments = Assessment.objects.filter(component=component, period=self.period)

            if not assessments.exists():
                continue

            total_perfect_score = assessments.aggregate(Sum('total_points'))['total_points__sum'] or 0

            student_scores = StudentScore.objects.filter(
                enrollment=self.enrollment,
                assessment__in=assessments
            ).aggregate(Sum('score'))['score__sum'] or 0

            if total_perfect_score > 0:
                transmuted_grade = (float(student_scores) / float(total_perfect_score)) * 40 + 60
                weighted_score = transmuted_grade * (float(component.weight_percentage) / 100)
                total_period_grade += weighted_score

        self.computed_grade = round(total_period_grade, 2)
        self.save()

        return self.computed_grade

    def __str__(self):
        return f"{self.enrollment.student.last_name} - {self.period.name}: {self.computed_grade}"
