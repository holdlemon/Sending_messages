from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .tasks import send_notification
from notifications.serializers import NotificationSerializer


class NotificationAPIView(APIView):
    """ Представление для обработки POST-запроса """

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            notification = serializer.save()
            delay_seconds = {
                0: 0,
                1: 3600,
                2: 86400
            }.get(notification.delay)
            send_notification.apply_async(args=[notification.id], countdown=delay_seconds)
            return Response({'status': 'success', 'notification_id': notification.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
