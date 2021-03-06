from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from .forms import UnregisterForm, RegisterForm
from .models import Workshop, WorkshopRegistration
from .registrations import handle_registration, handle_unregistration


def index(request):
    workshops = Workshop.objects.filter(open=True).exclude(workshopregistration__in=WorkshopRegistration.objects.filter(
        participant=request.user.id,
        active=True
    ))
    return render(request, 'index.html', {'workshops': workshops})


@login_required
def my_registrations(request):
    registration = WorkshopRegistration.objects.filter(participant_id=request.user.id, active=True).select_related(
        'workshop')
    return render(request, 'my_registrations.html', {'registration': registration})


@login_required
def register_form(request, idx: int):
    workshop = get_object_or_404(Workshop, pk=idx)
    form = RegisterForm(request.POST or None, workshop_id=idx)

    if request.method == 'POST' and form.is_valid():
        registration = WorkshopRegistration(workshop=workshop,
                                            participant=request.user)
        registered = False
        with transaction.atomic():
            if WorkshopRegistration.objects.filter(workshop=workshop, participant=request.user,
                                                   active=True).count() == 0:
                registration.save()
                registered = True
                question_ids = [str(w.id) for w in workshop.question_set.all()]
                for que_id in form.cleaned_data:
                    if que_id in question_ids:
                        registration.answers.create(text=form.cleaned_data[que_id], question_id=que_id)
                    else:
                        raise SuspiciousOperation('Invalid question id')
        if registered:
            handle_registration(workshop, registration, request)
        return redirect('workshop:my_registrations')

    return render(request, 'register_form.html', {'workshop': workshop, 'form': form})


@login_required
def unregister_form(request):
    form = UnregisterForm(request.POST)
    if form.is_valid():
        registration = get_object_or_404(WorkshopRegistration, pk=form.cleaned_data['registration_id'])
        if registration.participant.id == request.user.id:
            registration.active = False
            registration.save()
            handle_unregistration(registration, request)
        else:
            raise HttpResponseForbidden
    return redirect('workshop:my_registrations')
