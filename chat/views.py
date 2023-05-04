from django.utils.functional import cached_property
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from chat.models import Thread, Message
from chat.serializers import ThreadSerializer, ThreadCreateSerializer, MessageSerializer


class ThreadPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 20


class ThreadViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = ThreadSerializer
    queryset = Thread.objects.all()
    pagination_class = ThreadPagination

    def get_serializer_class(self):
        serializers = {
            "list": ThreadSerializer,
            "create": ThreadCreateSerializer,
            "retrieve": ThreadSerializer,
        }
        return serializers[self.action]

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("participants")
        user = self.request.GET.get("user")

        if self.request.user.is_staff:
            if user:
                queryset = queryset.filter(participants=user)
            else:
                queryset = queryset.filter(participants=self.request.user)
        else:
            queryset = queryset.filter(participants=self.request.user)
        return queryset


class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 40


class MessageViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Message.objects.all().select_related("thread", "sender")
    serializer_class = MessageSerializer
    pagination_class = MessagePagination

    @cached_property
    def thread(self):
        thread_id = self.kwargs.get("threads_pk")
        try:
            thread = Thread.objects.get(id=thread_id)
        except Thread.DoesNotExist:
            raise NotFound("A thread with given id does not exist")
        return thread

    def get_queryset(self):
        return self.queryset.filter(thread=self.thread).filter(thread__participants=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(sender=self.request.user, thread=self.thread)

    @action(
        methods=["GET"],
        url_path="mark_as_read",
        detail=True,
    )
    def mark_as_read(self, request, pk=None, threads_pk=None):
        message_id = self.kwargs.get("pk")
        try:
            message = Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            raise NotFound("A message with given id does not exist")
        message.is_read = True
        message.save()
        serializer = MessageSerializer(message)

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def unread_messages(request):
    unread_messages = Message.objects.filter(sender=request.user).filter(is_read=False).prefetch_related("thread")
    threads_with_unread_messages = []
    for messages in unread_messages:
        threads_with_unread_messages.append(messages.thread.id)
    number_of_unread_messages = unread_messages.count()
    return Response(
        {"number_of_unread_messages": number_of_unread_messages,
         "threads": set(threads_with_unread_messages)},
        status=status.HTTP_200_OK
    )
