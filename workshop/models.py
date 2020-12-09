from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


def get_name(self):
    return self.first_name + ' ' + self.last_name


User.add_to_class("__str__", get_name)


class Location(models.Model):
    address = models.CharField(max_length=200)
    short = models.CharField(max_length=50)

    def __str__(self):
        return self.short


class Workshop(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    open = models.BooleanField(default=True)
    auto_response = models.BooleanField(default=False)
    slots = models.IntegerField()
    speaker = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Question(models.Model):
    text = models.CharField(max_length=400)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['id']


class AnswerOption(models.Model):
    text = models.CharField(max_length=settings.MAX_ANSWER_LENGTH)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['id']


class WorkshopRegistration(models.Model):
    class Status(models.TextChoices):
        ACCEPTED = 'AC', _('Accepted')
        REJECTED = 'RE', _('Rejected')
        WAITING = 'WA', _('Waiting')
        WAITING_LIST = 'WL', _('Waiting List')

    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)
    accepted = models.CharField(max_length=2, choices=Status.choices, default=Status.WAITING)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.workshop.__str__() + ' | ' + self.participant.__str__()


class RegistrationAnswer(models.Model):
    workshop_registration = models.ForeignKey(WorkshopRegistration, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=settings.MAX_ANSWER_LENGTH)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('workshop_registration', 'question'),)
        ordering = ['id']

    def __str__(self):
        return self.text
