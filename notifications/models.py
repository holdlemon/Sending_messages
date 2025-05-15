import re
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class Notification(models.Model):
    """ Модель уведомления """

    DELAY_CHOICES = (
        (0, 'Без задержки'),
        (1, 'Через 1 час'),
        (2, 'Через 1 день')
    )
    message = models.TextField(max_length=1024, verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    delay = models.IntegerField(choices=DELAY_CHOICES, default=0, verbose_name='Задержка')

    def __str__(self):
        return f'Уведомление №{self.pk}'

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'


class Recipient(models.Model):
    """ Модель получателя """

    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='recipients', verbose_name='Уведомление')
    address = models.CharField(max_length=150, verbose_name='Адрес получателя')
    is_telegram = models.BooleanField(default=False, verbose_name='Телеграм')

    def save(self, *args, **kwargs):
        """ Определяем тип адреса (email или Tg) """
        if re.fullmatch(r'\d{5,20}', self.address):
            self.is_telegram = True
        else:
            try:
                validate_email(self.address)
                self.is_telegram = False
            except ValidationError:
                raise ValidationError(f'Неверный адрес получателя: {self.address}')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Адрес: {self.address}'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'


class DeliveryLog(models.Model):
    """ Модель лога отправки """

    STATUS_CHOISES = (
        ('pending', 'Ожидание'),
        ('success', 'Успешно'),
        ('failed', 'Неудачно')
    )
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, verbose_name='Уведомление')
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, verbose_name='Получатель')
    status = models.CharField(max_length=10, choices=STATUS_CHOISES, default='pending', verbose_name='Статус')
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='Время попытки')
    error_message = models.TextField(blank=True, null=True, verbose_name='Сообщение об ошибке')

    def __str__(self):
        return f'Лог отправки сообщения: {self.recipient} - {self.status}'

    class Meta:
        verbose_name = 'Лог отправки'
        verbose_name_plural = 'Логи отправки'
