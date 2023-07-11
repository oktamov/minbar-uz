from django.db import models
from django.db.models import Sum


class Quiz(models.Model):
    title = models.CharField(max_length=600)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Choice(models.Model):
    answer = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='choices')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.question.title} -> {self.answer}'

    @property
    def percent(self):
        total_votes = self.question.choices.aggregate(Sum('votes'))['votes__sum']
        if total_votes:
            percentage = (self.votes / total_votes) * 100
            return int(percentage)
        return 0


class Category(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title