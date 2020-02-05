from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Workshop


def index(request):
    workshops = Workshop.objects.filter(open=True)
    return render(request, 'index.html', {'workshops': workshops})


@login_required
# TODO: forms
def register_form(request, idx: int):
    workshop = get_object_or_404(Workshop, pk=idx)
    return render(request, 'register_form.html', {'workshop': workshop})
