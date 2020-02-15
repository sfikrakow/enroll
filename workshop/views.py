from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView

from .forms import UnregisterForm, RegisterForm
from .mail import send_workshop_cancelled
from .models import Workshop, WorkshopRegistration, RegistrationAnswer, Question


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
def register_form(request, idx: int):
    workshop = get_object_or_404(Workshop, pk=idx)
    form = RegisterForm(request.POST or None, workshop_id=idx)
    if request.method == 'POST':
        if form.is_valid():
            registration = WorkshopRegistration(workshop=workshop,
                                                participant=request.user)
            registration.save()
            for que_id in form.cleaned_data:
                question = get_object_or_404(Question, pk=que_id)
                reg_ans = RegistrationAnswer(workshop_registration=registration,
                                             question=question,
                                             text=form.cleaned_data[que_id])
                reg_ans.save()
            return redirect('/registrations')

    return render(request, 'register_form.html', {'workshop': workshop, 'form': form})


@login_required
def unregister_form(request):
    form = UnregisterForm(request.POST)
    if form.is_valid():
        registration = get_object_or_404(WorkshopRegistration, pk=form.cleaned_data['registration_id'])
        if registration.participant.id == request.user.id:
            registration.active = False
            registration.save()
            send_workshop_cancelled(registration.workshop, request.user, request)
            # TODO: handle unregistration
        else:
            raise HttpResponseForbidden
    return redirect('workshop:my_registrations')
