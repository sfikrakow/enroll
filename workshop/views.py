from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView

from .forms import UnregisterForm
from .models import Workshop, WorkshopRegistration


def index(request):
    workshops = Workshop.objects.filter(open=True).exclude(workshopregistration__participant_id=request.user.id,
                                                           workshopregistration__active=True)
    return render(request, 'index.html', {'workshops': workshops})


@login_required
def my_registrations(request):
    registration = WorkshopRegistration.objects.filter(participant_id=request.user.id, active=True).select_related(
        'workshop')
    return render(request, 'my_registrations.html', {'registration': registration})


@login_required
# TODO: form (formview?)
def register_form(request, idx: int):
    workshop = get_object_or_404(Workshop, pk=idx)
    return render(request, 'register_form.html', {'workshop': workshop})


@login_required
def unregister_form(request):
    form = UnregisterForm(request.POST)
    if form.is_valid():
        registration = get_object_or_404(WorkshopRegistration, pk=form.cleaned_data['registration_id'])
        if registration.participant.id == request.user.id:
            registration.active = False
            registration.save()
            # TODO: handle unregistration
        else:
            raise HttpResponseForbidden
    return redirect('workshop:my_registrations')
