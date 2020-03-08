from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.datetime_safe import datetime
from ics import Calendar, Event, Attendee, Organizer

from workshop.models import Workshop


class SFImailMessage(EmailMultiAlternatives):
    def __init__(self, template_name: str, template_params: dict, subject: str, recipient_list: list, request):
        body_text = render_to_string(template_name + '.txt', template_params, request)
        body_html = render_to_string(template_name + '.html', template_params, request)

        super().__init__(body=body_text, subject=subject, from_email=settings.DEFAULT_FROM_EMAIL, to=recipient_list,
                         reply_to=[settings.DEFAULT_REPLY_TO_EMAIL])
        self.attach_alternative(body_html, 'text/html')

    def send(self, fail_silently=False):
        return super().send(fail_silently or settings.EMAIL_FAIL_SILENTLY)


def _create_workshop_params(header, workshop, request):
    return {
        'header': header,
        'date': workshop.start_date,
        'location': workshop.location,
        'speaker': workshop.speaker,
        'describtion': workshop.description,
        'site_url': request.build_absolute_uri(reverse('workshop:my_registrations'))
    }


class ICALWorkshop:
    def __init__(self, workshop: Workshop, user: settings.AUTH_USER_MODEL):
        self._event = Event()
        self._calender = Calendar(creator='-//Studencki Festiwal Informatyczny//Enroll//EN', events=[self._event])
        self._event.begin = workshop.start_date
        self._event.end = workshop.end_date
        self._event.description = workshop.speaker + '\n' + workshop.description
        self._event.name = '[SFI] ' + workshop.name
        self._event.location = workshop.location.address
        self._event.organizer = Organizer(settings.DEFAULT_REPLY_TO_EMAIL, settings.DEFAULT_REPLY_TO_EMAIL)
        self._event.uid = 'workshop-{}@workshops.sfi.pl'.format(workshop.id)
        self._event.created = datetime.now()
        self._event.add_attendee(Attendee(user.email, user.email, 'TRUE'))
        self._event.transparent = "OPAQUE"

    def get_confirmed_event(self):
        self._event.status = 'CONFIRMED'
        self._calender.method = 'REQUEST'
        return str(self._calender).replace('RSVP=TRUE', 'ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE')

    def get_canceled_event(self):
        self._event.status = 'CANCELLED'
        self._calender.method = 'CANCEL'
        return str(self._calender)


def send_workshop_confirmation(workshop: Workshop, participant: settings.AUTH_USER_MODEL, request):
    message = SFImailMessage('mail/workshop', _create_workshop_params(
        'Twoja rejestracja na {} została zaakceptowana!'.format(workshop.name), workshop, request),
                             '[SFI] Rejestracja na warsztaty', [participant.email], request)
    message.attach('event.ics', ICALWorkshop(workshop, participant).get_confirmed_event(),
                   'text/calendar; method=REQUEST')
    message.send()


def send_workshop_pending(workshop: Workshop, participant: settings.AUTH_USER_MODEL, request):
    message = SFImailMessage('mail/workshop', _create_workshop_params(
        'Twoja rejestracja na {} oczekuje na akceptację'.format(workshop.name), workshop, request),
                             '[SFI] Rejestracja na warsztaty', [participant.email], request)
    message.send()


def send_workshop_waiting_list(workshop: Workshop, participant: settings.AUTH_USER_MODEL, request):
    message = SFImailMessage('mail/basic', {
        'header': 'Wpisaliśmy Cię na listę rezerwową na {}'.format(workshop.name),
        'content': 'Niestety wszystkie miejsca są już zajęte, ale wpisaliśmy Cię na listę rezerwową.' +
                   ' Jeśli zwolni się dla Ciebie miejsce poinformujemy Cię o tym mailowo.',
        'site_url': request.build_absolute_uri(reverse('workshop:my_registrations'))
    }, '[SFI] Rejestracja na warsztaty', [participant.email], request)
    message.send()


def send_workshop_cancelled(workshop: Workshop, participant: settings.AUTH_USER_MODEL, request, was_accepted):
    message = SFImailMessage('mail/basic', {
        'header': 'Twoja rejestracja na {} została anulowana'.format(workshop.name),
        'content': 'Anulowaliśmy rejestrację na Twoją prośbę.',
        'site_url': request.build_absolute_uri(reverse('workshop:my_registrations'))
    }, '[SFI] Rejestracja na warsztaty', [participant.email], request)
    if was_accepted:
        message.attach('event.ics', ICALWorkshop(workshop, participant).get_canceled_event(),
                       'text/calendar; method=CANCEL')
    message.send()


def send_workshop_rejected(workshop: Workshop, participant: settings.AUTH_USER_MODEL, request):
    message = SFImailMessage('mail/basic', {
        'header': 'Twoja rejestracja na {} została odrzucona'.format(workshop.name),
        'content': 'Niestety wszystkie miejsca na tych warsztatach zostąły już przydzielone.',
        'site_url': request.build_absolute_uri(reverse('workshop:my_registrations'))
    }, '[SFI] Rejestracja na warsztaty', [participant.email], request)
    message.attach('event.ics', ICALWorkshop(workshop, participant).get_canceled_event(),
                   'text/calendar; method=CANCEL:')
    message.send()
