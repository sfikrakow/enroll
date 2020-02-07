from django.forms import Form, IntegerField


class UnregisterForm(Form):
    registration_id = IntegerField()
