from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.formats import date_format

from workshop.models import Workshop


class SFImailMessage(EmailMultiAlternatives):
    def __init__(self, template_name: str, template_params: dict, subject: str, recipient_list: list):
        body_text = render_to_string(template_name + '.txt', template_params)
        body_html = render_to_string(template_name + '.html', template_params)

        super().__init__(body=body_text, subject=subject, from_email=settings.DEFAULT_FROM_EMAIL, to=recipient_list,
                         reply_to=[settings.DEFAULT_REPLY_TO_EMAIL])
        self.attach_alternative(body_html, 'text/html')

    def send(self, fail_silently=False):
        return super().send(fail_silently or settings.EMAIL_FAIL_SILENTLY)


def _create_workshop_params(header, workshop, request):
    return {
        'header': header,
        'date': date_format(workshop.date, 'j E Y, H:i'),
        'location': workshop.location,
        'speaker': workshop.speaker,
        'describtion': workshop.description,
        'site_url': request.build_absolute_uri(reverse('workshop:my_registrations'))
    }


def send_workshop_confirmation(workshop: Workshop, participant: settings.AUTH_USER_MODEL, request):
    message = SFImailMessage('mail/workshop', _create_workshop_params(
        'Twoja rejestracja na {} została zaakceptowana!'.format(workshop.name), workshop, request),
                             '[SFI] Rejestracja na warsztaty', [participant.email])
    message.send()


def send_workshop_pending(workshop: Workshop, participant: settings.AUTH_USER_MODEL, request):
    message = SFImailMessage('mail/workshop', _create_workshop_params(
        'Twoja rejestracja na {} oczekuje na akceptację'.format(workshop.name), workshop, request),
                             '[SFI] Rejestracja na warsztaty', [participant.email])
    message.send()


def send_workshop_waiting_list(workshop: Workshop, participant: settings.AUTH_USER_MODEL, request):
    message = SFImailMessage('mail/basic', {
        'header': 'Wpisaliśmy Cię na listę rezerwową na {}'.format(workshop.name),
        'content': 'Niestety wszystkie miejsca są już zajęte, ale wpisaliśmy Cię na listę rezerwową.' +
                   ' Jeśli zwolni się dla Ciebie miejsce poinformujemy Cię o tym mailowo.',
        'site_url': request.build_absolute_uri(reverse('workshop:my_registrations'))
    }, '[SFI] Rejestracja na warsztaty', [participant.email])
    message.send()


def send_workshop_cancelled(workshop: Workshop, participant: settings.AUTH_USER_MODEL, request):
    message = SFImailMessage('mail/basic', {
        'header': 'Twoja rejestracja na {} została anulowana'.format(workshop.name),
        'content': 'Anulowaliśmy rejestrację na Twoją prośbę.',
        'site_url': request.build_absolute_uri(reverse('workshop:my_registrations'))
    }, '[SFI] Rejestracja na warsztaty', [participant.email])
    message.send()


def send_workshop_rejected(workshop: Workshop, participant: settings.AUTH_USER_MODEL, request):
    message = SFImailMessage('mail/basic', {
        'header': 'Twoja rejestracja na {} została odrzucona'.format(workshop.name),
        'content': 'Niestety wszystkie miejsca na tych warsztatach zostąły już przydzielone.',
        'site_url': request.build_absolute_uri(reverse('workshop:my_registrations'))
    },
                             '[SFI] Rejestracja na warsztaty', [participant.email])
    message.send()
