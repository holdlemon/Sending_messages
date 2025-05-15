from celery import shared_task
from .models import Notification, DeliveryLog
from django.core.mail import send_mail
from django.conf import settings
import os
import requests


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_notification(self, notification_id):
    """ Celery-задача для отправки уведомления """
    try:
        notification = Notification.objects.get(id=notification_id)
        for recipient in notification.recipients.all():
            log = DeliveryLog.objects.create(notification=notification, recipient=recipient, status='pending')

            try:
                if recipient.is_telegram:
                    token = os.getenv("BOT_TOKEN")
                    response = requests.post(
                        f"https://api.telegram.org/bot{token}/sendMessage",
                        data={
                            'chat_id': recipient.address,
                            'text': notification.message
                        }
                    )
                    if response.status_code != 200:
                        raise Exception(response.json().get('description', 'Ошибка Telegram API'))
                else:
                    send_mail(
                        'Notification',
                        notification.message,
                        settings.DEFAULT_FROM_EMAIL,
                        [recipient.address],
                        fail_silently=True
                    )
                log.status = 'success'
            except Exception as e:
                log.status = 'failed'
                log.error_message = str(e)
                self.retry(exc=e)
            finally:
                log.save()
        return True

    except Notification.DoesNotExist:
        return False
