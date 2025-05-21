from rest_framework import serializers
from .models import Notification, Recipient


class NotificationSerializer(serializers.Serializer):
    """ Сериализатор для входящего запроса на api/notify/ """

    message = serializers.CharField(max_length=1024, label='Сообщение')
    recipient = serializers.JSONField(label='Получатель')
    delay = serializers.IntegerField(min_value=0, max_value=2, label='Задержка')

    def validate_recipient(self, value):
        """ Приводим к списку строк """

        if isinstance(value, str):
            return [value]
        if isinstance(value, list) and all(isinstance(i, str) for i in value):
            return value
        raise serializers.ValidationError('Поле "recipient" должно быть строкой или списком строк')

    def create(self, validated_data):
        """ Сохраняем записи в БД """

        recipients = validated_data.pop('recipient')
        notification = Notification.objects.create(**validated_data)
        for address in recipients:
            Recipient.objects.create(notification=notification, address=address)
        return notification
