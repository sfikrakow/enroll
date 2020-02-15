from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Location(models.Model):
    address = models.CharField(max_length=200)
    short = models.CharField(max_length=50)

    def __str__(self):
        return self.short


class Workshop(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    open = models.BooleanField(default=True)
    auto_response = models.BooleanField(default=False)
    slots = models.IntegerField()
    speaker = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.CharField(max_length=200)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.text


class DefaultAnswer(models.Model):
    text = models.CharField(max_length=settings.MAX_ANSWER_LENGTH)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class WorkshopRegistration(models.Model):
    class Status(models.TextChoices):
        ACCEPTED = 'AC', _('Zaakceptowane')
        REJECTED = 'RE', _('Odrzucone')
        WAITING = 'WA', _('Oczekujące')

    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)
    accepted = models.CharField(max_length=2, choices=Status.choices, default=Status.WAITING)
    active = models.BooleanField(default=True)


class RegistrationAnswer(models.Model):
    workshop_registration = models.ForeignKey(WorkshopRegistration, on_delete=models.CASCADE)
    text = models.CharField(max_length=settings.MAX_ANSWER_LENGTH)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)

    def __str__(self):
        return self.text
