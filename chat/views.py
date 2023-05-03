from rest_framework import viewsets, mixins, generics, status
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import NotFound, PermissionDenied
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
        user = self.request.GET.get("user")

        if self.request.user.is_staff:
            if user:
                return self.queryset.filter(participants=user)
            else:
                return self.queryset.filter(participants=self.request.user)
        else:
            return self.queryset.filter(participants=self.request.user)


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
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = MessagePagination

    def get_queryset(self):
        thread_id = self.kwargs.get("threads_pk")
        try:
            thread = Thread.objects.get(id=thread_id)
        except Thread.DoesNotExist:
            raise NotFound("A thread with given id does not exist")
        if self.request.user not in thread.participants.all():
            raise PermissionDenied(
                {"message": "You do not have access"}
            )
        return self.queryset.filter(thread=thread).filter(thread__participants=self.request.user)

    def perform_create(self, serializer):
        thread_id = self.kwargs.get("threads_pk")
        thread = generics.get_object_or_404(Thread, id=thread_id)
        return serializer.save(sender=self.request.user, thread=thread)

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
    unread_messages = Message.objects.filter(sender=request.user).filter(is_read=False)
    threads_with_unread_messages = []
    for messages in unread_messages:
        threads_with_unread_messages.append(messages.thread.id)
    number_of_unread_messages = unread_messages.count()
    return Response(
        {"number_of_unread_messages": number_of_unread_messages,
         "threads": set(threads_with_unread_messages)},
        status=status.HTTP_200_OK
    )
