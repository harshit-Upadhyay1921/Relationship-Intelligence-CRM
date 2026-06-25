from rest_framework.routers import DefaultRouter
from .views import InteractionViewSet

router = DefaultRouter()
router.register(r"interactions", InteractionViewSet)

urlpatterns = router.urls