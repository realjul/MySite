from django.db import models
from django.utils import timezone
from jobs.models import JobBase, Profile


# Create your models here.
class Exam(models.Model):
    SEASONS = (
        ('SPRING', 'Spring'),
        ('SUMMER', 'Summer'),
        ('FALL', 'Fall'),
        ('WINTER', 'Winter'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True,max_length=500)
    job = models.ForeignKey(JobBase,on_delete=models.CASCADE, related_name='exams')
    season = models.CharField(choices=SEASONS, max_length=10)
    year = models.PositiveIntegerField()
    passing_score = models.PositiveIntegerField(default=90)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('job', 'season', 'year')
        ordering = ['-year','-season']


    def __str__(self):
        return f"{self.job.title} Exam - ({self.get_season_display()} {self.year})"

class Question(models.Model):
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.exam.title} Q{self.order}: {self.text[:50]}"
    class Meta:
        ordering = ('order',)


class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Choice for Q{self.question.id}: {self.text[:40]}"


class ExamResult(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.FloatField()
    passed = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
