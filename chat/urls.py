from rest_framework.routers import DefaultRouter

from chat.views import ThreadViewSet

router = DefaultRouter()

router.register("threads", ThreadViewSet)

urlpatterns = router.urls


app_name = "chat"
