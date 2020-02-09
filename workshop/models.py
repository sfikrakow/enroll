from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Workshop(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    open = models.BooleanField(default=True)
    auto_response = models.BooleanField(default=False)
    slots = models.IntegerField()
    speaker = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.CharField(max_length=200)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class DefaultAnswer(models.Model):
    text = models.CharField(max_length=settings.MAX_ANSWER_LENGTH)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class WorkshopRegistration(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)
    active = models.BooleanField()
    accepted = models.BooleanField()


class RegistrationAnswer(models.Model):
    workshop_registration = models.ForeignKey(WorkshopRegistration, on_delete=models.CASCADE)
    text = models.CharField(max_length=settings.MAX_ANSWER_LENGTH)

    def __str__(self):
        return self.text
