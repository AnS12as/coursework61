from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .models import Mailing, MailingAttempt
import pytz


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', minutes=10)
    scheduler.start()


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = timezone.now()
    mailings = Mailing.objects.filter(start_datetime__lte=current_datetime, status='created')

    for mailing in mailings:
        for client in mailing.clients.all():
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                server_response = 'Email sent successfully'
                status = True
            except Exception as e:
                server_response = str(e)
                status = False

            MailingAttempt.objects.create(
                mailing=mailing,
                status=status,
                server_response=server_response
            )

        if mailing.periodicity == 'daily':
            next_send_time = mailing.start_datetime + timezone.timedelta(days=1)
        elif mailing.periodicity == 'weekly':
            next_send_time = mailing.start_datetime + timezone.timedelta(weeks=1)
        elif mailing.periodicity == 'monthly':
            next_send_time = mailing.start_datetime + timezone.timedelta(weeks=4)

        mailing.start_datetime = next_send_time
        mailing.save()
