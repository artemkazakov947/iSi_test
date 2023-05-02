from django.urls import path, include
from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter
from chat.views import ThreadViewSet, MessageViewSet

router = SimpleRouter()

router.register("threads", ThreadViewSet)

message_router = NestedSimpleRouter(
    router,
    r"threads",
    lookup="threads"
)

message_router.register(
    r"messages",
    MessageViewSet,
    basename="threads-messages"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(message_router.urls))
]


app_name = "chat"
