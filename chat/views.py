from rest_framework import viewsets, mixins

from chat.models import Thread
from chat.serializers import ThreadSerializer, ThreadCreateSerializer


class ThreadViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = ThreadSerializer
    queryset = Thread.objects.all()

    def get_serializer_class(self):
        serializers = {
            "list": ThreadSerializer,
            "create": ThreadCreateSerializer,
            "retrieve": ThreadSerializer,
        }
        return serializers[self.action]

    def get_queryset(self):
        user = self.request.GET.get("user")

        if self.request.user.is_staff:
            if user:
                return self.queryset.filter(participants=user)
            else:
                return self.queryset.filter(participants=self.request.user)
        else:
            return self.queryset.filter(participants=self.request.user)
