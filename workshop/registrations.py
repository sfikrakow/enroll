from .mail import send_workshop_cancelled, send_workshop_confirmation, send_workshop_pending, \
    send_workshop_waiting_list
from .models import WorkshopRegistration, Workshop


def workshop_free_seats(workshop: Workshop):
    return workshop.slots - WorkshopRegistration.objects.filter(workshop=workshop, active=True,
                                                                accepted=WorkshopRegistration.Status.ACCEPTED).count()


def workshop_accept_first(workshop: Workshop, request):
    waiting_list = WorkshopRegistration.objects.filter(workshop=workshop,
                                                       accepted=WorkshopRegistration.Status.WAITING_LIST,
                                                       active=True).order_by('date')
    if workshop_free_seats(workshop) > 0 and len(waiting_list) > 0:
        reg = waiting_list[0]
        reg.accepted = WorkshopRegistration.Status.ACCEPTED
        reg.save()
        send_workshop_confirmation(workshop, reg.participant, request)


def handle_registration(workshop: Workshop, registration: WorkshopRegistration, request):
    if workshop.auto_response:
        if workshop_free_seats(workshop) > 0:
            registration.accepted = WorkshopRegistration.Status.ACCEPTED
            registration.save()
            send_workshop_confirmation(workshop, request.user, request)
        else:
            registration.accepted = WorkshopRegistration.Status.WAITING_LIST
            registration.save()
            send_workshop_waiting_list(workshop, request.user, request)
    else:
        send_workshop_pending(workshop, request.user, request)


def handle_unregistration(registration: WorkshopRegistration, request):
    send_workshop_cancelled(registration.workshop, request.user, request,
                            registration.accepted == WorkshopRegistration.Status.ACCEPTED)
    if registration.accepted == WorkshopRegistration.Status.ACCEPTED and registration.workshop.auto_response:
        workshop_accept_first(registration.workshop, request)
