from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Workshop(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    open = models.BooleanField(default=True)
    auto_response = models.BooleanField(default=False)

    def __str__(self):
        return self.name + '(' + str(self.id) + ')'


class WorkshopRegistration(models.Model):
    workshops_id = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    participant_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=now)
    active = models.BooleanField()
    accepted = models.BooleanField()
