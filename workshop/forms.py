from django.forms import Form, IntegerField, CharField
from .models import Question, Workshop, AnswerOption, RegistrationAnswer, WorkshopRegistration
import django.forms as forms
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect


class RegisterForm(Form):
    def __init__(self, *args, **kwargs):
        workshop_id = kwargs.pop('workshop_id')
        super(RegisterForm, self).__init__(*args, **kwargs)

        questions = Question.objects.filter(workshop=workshop_id, active=True)
        for q in questions:
            ans = AnswerOption.objects.filter(question=q.id)
            if ans.count() > 0:
                self.fields[str(q.id)] = forms.ModelChoiceField(queryset=ans, empty_label=None,
                                                                widget=forms.RadioSelect())
            else:
                self.fields[str(q.id)] = forms.CharField(max_length=settings.MAX_ANSWER_LENGTH,
                                                         widget=forms.TextInput())
            self.fields[str(q.id)].label = q.text


class UnregisterForm(Form):
    registration_id = IntegerField()
